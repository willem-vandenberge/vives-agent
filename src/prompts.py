# prompts voor de LLM

class DeveloperToolsPrompts:
    """ Gebruikte prompts voor applicatie """

    # Nieuws samenvatter
    NEWS_SUMMARY_ASSISTANT= """Je bent een assistent die artikelen kort en bondig samenvat in het Nederlands."""

    @staticmethod
    def news_summarizer_user(content: str) -> str:
        return f"""
                    Vat het volgende artikel samen in maximaal 5 zinnen:
                    Article Content: {content}
                    
                    output: 
                    - summary: de samenvatting van het artikel
                """

    # Nieuws samenvatter

    NEWS_FACT_CHECKER_ASSISTANT="""
                                    Je bent een journalist met jaren ervaring en enorme hoeveelheid kennis.
                                    Jouw taak is om artikels na te lezen en kijken of ze feitelijk kloppen.
                                    Maak géén claims over feiten die zich afspeelden na jouw kennisdatum, deze feiten
                                    mogen ook jouw beslissing niet beïnvloeden.
                                """

    @staticmethod
    def news_fact_checker_user(content: str) -> str:
        return f"""
                        Ga na indien het volgende artikel feitelijk juist is. Geef ook aan waarom wel of niet.
                        Baseer je enkel op informatie van voor je kennisdatum. Feiten die zich afspelen na deze datum
                        mag je niet gebruiken om een artikel als niet feitelijk correct te zien. 
                        Controleer dus enkel de nieuwsfeiten van voor je kennisdatum, en gebruik deze om een inschatting 
                        te maken over de feitelijke juistheid van het artikel.
                        
                        Article Content: {content}
                        Analyzeer het artikel en geef:
                        - is_feitelijk_correct: true indien je het artikel feitelijk juist vind, false indien niet.
                        - verklaring: korte uitleg waarom het artikel niet correct is. 
                """

    @staticmethod
    def extract_article_query(num_results: int = 10) -> str:
        return f"""
                    On HLN.be's 'NIEUWS' page, find all the articles published today.
                    For each listed item, extract the title, URL, a one-sentence summary and if the article is a 'plus' article.
                    Only take the first {num_results} items.
                """
    @staticmethod
    def article_summary(query: str, content: str) -> str:
        return f"""Query: {query}
                Artikel inhoud: {content}
                
                
                """
