#

from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from .models import ResearchState, ArticleAnalysis, NewsArticle
from .firecrawl import FirecrawlService
from .prompts import DeveloperToolsPrompts


class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1) # lagere temp = "correcter"
        self.prompts = DeveloperToolsPrompts()
        self.workflow = self._build_workflow()

    """
        Met langgraph een workflow aanmaken die onze Agent zal volgen.  (39:52)
        Graph met stages
    """
    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        # Stap 1 : Nieuwssite(s) extracten, en volledige tekst ophalen
        graph.add_node("extract_articles", self._extract_articles_step)

        # stap 2 : Artikels samenvatten
        graph.add_node("summarize_articles", self._generate_articles_summary)

        # Stap 4 : Artikels factchecken
        graph.add_node("fact_check_articles", self._check_truth_articles)

        # stap 5 : Nieuwsoverzicht weergeven

        # start, eindpunt en volgorde van de graph definiëren
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
        SCRAPE: haald enkel de content van die url op (géén links)
        SEARCH voert een websearch uit gebruikmakend vna een query
        CRAWL: volgt ook de aanwezige links op de pagina
    """
    def _extract_articles_step(self, state: ResearchState) -> Dict[str, Any]:
        print(f"🔍 Meest gelezen artikels zoeken: {state.query}")

        article_query = f"{self.prompts.extract_article_query(10)}"

        # Met extract artikels ophalen
        # search_results = self.firecrawl.extract_articles(article_query, num_results=10)
        # TIJDENS TESTEN DUMMY METHODE GEBRUIKEN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        search_results = self.firecrawl.extract_dummy_articles()

        print(search_results)
        # artikels toevoegen aan de researchstate
        articles = getattr(state, "articles", [])

        # De gekozen urls ophalen
        for result in search_results:
            newsArticle = NewsArticle(url=result['url'],
                                      title=result['title'],
                                      summary=result['summary'],
                                      is_trustworthy=result['plus'])

            # TEST CODE !!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #extracted_body = self.firecrawl.extract_full_article(newsArticle.url)
            extracted_body = self.firecrawl.extract_dummy_article_content()
            if extracted_body:
                # alle content ?? limiet om niet te veel in model te steken (ifv tokens)
                newsArticle.full_text = extracted_body
            articles.append(newsArticle)

            break # break uit loop om aantal resultaten te beperken

        return {"articles": articles}




    """
        STAP 2: Artikel samenvatten
        Artikels samenvatten
        @:return samengevatte artikels -> lijst? 
    """
    def _generate_articles_summary(self, state: ResearchState):
        # artikels samenvatten
        articles = state.articles
        # meegeven aan llm wat je wil
        summary_llm = self.llm

        for article in articles:
            # berichten voor llm
            messages = [
                SystemMessage(content=self.prompts.NEWS_SUMMARY_ASSISTANT),
                HumanMessage(content=self.prompts.news_summarizer_user(article.full_text))
            ]

            try:
                #summary = summary_llm.invoke(messages)
                #article.summary = summary
                # return analysis
                print("generating summary")
                #print(summary)
            except Exception as e:
                print(e)
        # We passen hier opnieuw de Researchstate aan voor de volgende stap
        return {"articles": articles}

    """
           Artikels samenvatten
           @:return samengevatte artikels -> lijst? 
       """
    def _check_truth_articles(self, state: ResearchState):
        # aan llm vragen of via web om te checken ????????!!!!!
        articles = state.articles

        # meegeven aan llm wat je wil, een model met verwachte output
        fact_checker_llm = self.llm.with_structured_output(ArticleAnalysis)

        for article in articles:
            # berichten voor llm
            messages = [
                SystemMessage(content=self.prompts.NEWS_FACT_CHECKER_ASSISTANT),
                HumanMessage(content=self.prompts.news_fact_checker_user(article.full_text))
            ]

            try:
                article_alalysis = fact_checker_llm.invoke(messages)
                print(article_alalysis.is_factual_correct)
                print(article_alalysis.conclusion_explanation)

                # return analysis
                print("generating summary")
                #print(summary)
            except Exception as e:
                print(e)
        # We passen hier opnieuw de Researchstate aan voor de volgende stap
        return {"articles": articles}

    """
        @:param query: input van de user
    """
    def run(self, query: str) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = self.workflow.invoke(initial_state)
        return ResearchState(**final_state)