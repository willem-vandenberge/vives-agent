#

from typing import Dict, Any

from langchain_core.tools import tool, Tool
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode
from .models import ResearchState, ArticleAnalysis, NewsArticle, ArticleSummary
from .firecrawl import FirecrawlService
from .prompts import DeveloperToolsPrompts
from langchain.tools import StructuredTool
from langchain_community.tools import JinaSearch, DuckDuckGoSearchRun
from langchain_core.runnables import RunnableConfig, chain



class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()
        self.llm = ChatOpenAI(model="gpt-5", temperature=0.1)  # lagere temp = "correcter"
        self.prompts = DeveloperToolsPrompts()
        self.workflow = self._build_workflow()

    """
        Met langgraph een workflow aanmaken die onze Agent zal volgen.  (39:52)
        Graph met stages
    """
    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        # Stap 1 : Nieuwssite(s) ophalen
        graph.add_node("extract_articles", self._extract_articles_step)

        # stap 2 : Artikels fact checken
        graph.add_node("summarize_articles", self._generate_articles_summary)

        # Stap 3 : Artikels samenvatten
        graph.add_node("fact_check_articles", self._check_truth_articles)
        # graph.add_node("fact_check_articles", ToolNode([self._check_truth_articles]))

        # Volgorde graph vastleggen dmv edges
        graph.set_entry_point("extract_articles")
        graph.add_edge("extract_articles", "fact_check_articles")
        graph.add_edge("fact_check_articles", "summarize_articles")
        graph.add_edge("summarize_articles", END)

        return graph.compile()

    # private functies

    """
        STAP 1 : arttikels zoeken, artikels scrapen? 
        Scrape 10? artikels van een nieuwssite
        @:param state (42:00)
        @:return titels van 10 gekozen artikels
        
        SEARCH IPV SCRAPE ???!!!!!!
        SCRAPE: haalt enkel de content van die url op (géén links)
        SEARCH voert een websearch uit gebruikmakend vna een query
        CRAWL: volgt ook de aanwezige links op de pagina
    """

    def _extract_articles_step(self, state: ResearchState) -> Dict[str, Any]:
        print(f"🔍 Artikels artikels zoeken van de nieuws sectie van www.hln.be: ")

        article_query = f"{self.prompts.extract_article_query(2)}"

        # Met extract artikels ophalen
        search_results = self.firecrawl.extract_articles(num_results=10)
        # TIJDENS TESTEN DUMMY METHODE GEBRUIKEN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #search_results = self.firecrawl.extract_dummy_articles()

        print("---------Stap 1 artikels zoeken en volledig ophalen ------")
        print(search_results)

        # artikels toevoegen aan de researchstate
        articles = getattr(state, "articles", [])

        # De gekozen urls ophalen
        for result in search_results:
            # indien het een plus artikel is wordt het geskipt
            if not result["plus"]:

                newsArticle = NewsArticle(url=result['url'],
                                      title=result['title'],
                                      summary=result['summary'],
                                      is_trustworthy=result['plus'])

                # TEST CODE !!!!!!!!!!!!!!!!!!!!!!!!!!!!
                extracted_body = self.firecrawl.extract_full_article(newsArticle.url)
                #extracted_body = self.firecrawl.extract_dummy_article_content()
                if extracted_body:
                    # alle content ?? limiet om niet te veel in model te steken (ifv tokens)
                    newsArticle.full_text = extracted_body
                    print(newsArticle.full_text)
                articles.append(newsArticle)

                #break  # break uit loop om aantal resultaten te beperken

        return {"articles": articles}

    """
        STAP 3: Artikel samenvatten
        Artikels samenvatten
    """

    def _generate_articles_summary(self, state: ResearchState):
        print(" ---------------------------- Gefactcheckt Nieuwsoverzicht ----------------")
        # artikels samenvatten
        articles = state.articles
        # meegeven aan llm wat je wil
        summary_llm = self.llm.with_structured_output(ArticleSummary)


        for article in articles:
            # enkel betrouwbare artikels samenvatten en opnemen in het nieuwsoverzicht
            if article.is_trustworthy:
                # berichten voor llm
                messages = [
                    SystemMessage(content=self.prompts.NEWS_SUMMARY_ASSISTANT),
                    HumanMessage(content=self.prompts.news_summarizer_user(article.full_text))
                ]

                try:
                    summary = summary_llm.invoke(messages)
                    article.summary = summary.summary
                    print(summary.summary)
                except Exception as e:
                    print(e)
        # We passen hier opnieuw de Researchstate aan voor de volgende stap
        return {"articles": articles}

    """
           Artikels fact checken
    """
    def _check_truth_articles(self, state: ResearchState):
        # aan llm vragen of via web om te checken ????????!!!!!
        articles = state.articles
        tool = {"type" : "web_search_preview"}
        # meegeven aan llm wat je wil, een model met verwachte output
        fact_checker_llm = self.llm.with_structured_output(ArticleAnalysis)

        #llm_with_tools = llm.bind_tools([search_tool, json_schema_tool])
        print(" ------------------ stap 2: factchecken -----------------------")
        for article in articles:
            messages = [
                SystemMessage(content=self.prompts.NEWS_FACT_CHECKER_ASSISTANT),
                HumanMessage(content=self.prompts.news_fact_checker_user(article.full_text))
            ]
            try:
                article_alalysis = fact_checker_llm.invoke(messages)
                print(f"-> Is het artikel correct? titel: {article.title}")
                print(article_alalysis.is_factual_correct)
                print("-> Verklaring?")
                print(article_alalysis.conclusion_explanation)
                article.is_trustworthy = article_alalysis.is_factual_correct
            except Exception as e:
                print(e)
        # We passen hier opnieuw de Researchstate aan voor de volgende stap
        return {"articles": articles}

    """
        @:param query: input van de user
    """

    def run(self) -> ResearchState:
        initial_state = ResearchState()
        final_state = self.workflow.invoke(initial_state)
        return ResearchState(**final_state)
