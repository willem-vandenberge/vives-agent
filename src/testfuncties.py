
import os
from typing import Dict, Any

from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv
from .models import ResearchState, Article, MostReadList, FullArticle

"""
      Haal de 10 gekozen artikels op.

       @TODO: ARTIKELS HIER SAMENVATTEN ????!!!!
      @:return titel en inhoud van artikels
"""


def _scrape_chosen_articles_step(self, state: ResearchState) -> Dict[str, Any]:
    print(f"🔍 Scrape chosen articles: {state.query}")
    articles_query = f"{state.query}"

    # urls meegeven van de artikels die we willen
    # search_results = self.firecrawl.scrape_articles("www.vrt.be/vrtnws/nl/")
    print("Gekozen artikels ophalen")


"""
            Artikels ophalen met de extract functie van firecrawl.
            Je geeft obv een prompt aan welke data je wilt opahelen. 
            @:return SearchResult met param data, error, ..
"""


def extract_articles(self, url: str, num_results: 10):
    """
    prompt=f"On HLN.be's homepage, find the 'Meest gelezen' (most read) section. "
                   "For each listed item, extract the title, URL, a one-sentence summary and if the article is a 'plus' article."
                   f"Only take the first {num_results} items.",

    """

    try:
        results = self.app.extract(
            ["https://www.hln.be/binnenland/"],
            prompt=f"On HLN.be's 'NIEUWS' page, find all the articles published today."
                   "For each listed item, extract the title, URL, a one-sentence summary and if the article is a 'plus' article."
                   f"Only take the first {num_results} items.",

            schema=MostReadList.model_json_schema()
        )

        # artikels uit resultaat halen
        if results.success:
            articles = results.data['articles']
            return articles
        raise Exception("#######error Fetching articles failed")

    except Exception as e:
        print(e)
        return None