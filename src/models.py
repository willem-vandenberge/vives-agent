# Schema om data te structureren zodat LLM weet in welk formaat en type hij data moet 'gieten' (28:00)
#

from typing import List, Optional
# Met pydantic kunnen we data eenvoudig valideren en typeren, aan LLM zeggen hoe de tekst moet in object gegoten worden
from pydantic import BaseModel

class ArticleSummary(BaseModel):
    summary: str

class FullArticle(BaseModel):
    title: str
    body: str


# Schema voor een artikel dat opgehaald wordt van hln.
class Article(BaseModel):
    title: str  # Field(..., description="Headline of the article")
    url: str  # Field(..., description="Full URL to the article")
    summary: str  # Field(None, description ="Optional short summary")
    plus: bool  # Field(..., description="Is the article for subscribers only? 'plus' article")


class MostReadList(BaseModel):
    articles: list[Article]


""" Gestructureerde output voor nieuws artikel """


class NewsArticle(BaseModel):
    title: str
    url: str
    full_text: str = ""
    summary: str = ""  # A brief description of the article
    is_trustworthy: Optional[bool]
    is_members_only: Optional[bool] = None


""" 
    Researchstate : wordt meegegeven bij elke stap. 
    -> bevat vereiste info voor volgende stappen
"""


class ResearchState(BaseModel):
    #  lijst met gekozen artikels
    articles: List[NewsArticle] = []


"""
    Gestructureerde output voor LLM die nieuwsartikelen gaat analyseren indien deze feitelijk juist zijn. 
    Zo weet de LLM in welke vorm het resultaat moet geretourneerd worden
"""


class ArticleAnalysis(BaseModel):
    is_factual_correct: bool
    conclusion_explanation: str
