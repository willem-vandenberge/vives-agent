# Alle firecrawl gerelateerde functionaliteit

import os
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import custom_tool

from .models import ResearchState, Article, MostReadList, FullArticle

load_dotenv()


class FirecrawlService:
    # constructor
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        self.app = FirecrawlApp(api_key=api_key)



    """
            Volledig artikel ophalen met de extract functie van firecrawl.
            mbv een prompt aangeven dat we de tekst van het artikel willen. 
            @:return body met tekst van het artikel
    """
    def extract_full_article(self, url: str):
        try:
            result = self.app.extract(
                [url],
                prompt="Extract the article's headline and full text. Wait until the page is fully loaded ",
                schema=FullArticle.model_json_schema()
            )

            # body uit resultaat halen
            if result.success:
                body = result.data['body']
                return body

            # Error opgooien wanneer fetch niet gelukt is
            raise Exception("#######error Fetching the full article")
        except Exception as e:
            print(e)
            return None



    """
        Functie voor het ophalen van de nieuwsartikelen.
        Scrapen gebruik je wanneer je urls hebt
        
        WAAR WORDT GEPROMPT HOEVEEL & WELKE ARTIKELS???
    """

    def scrape_article(self, url: str):
        try:
            result = self.app.scrape_url(
                url,
                formats=["markdown"],
                wait_for=12000,
                only_main_content=True

            )
            return result
        except Exception as e:
            print(e)
            return None


    def scrape_articles(self, url: str):
        try:
            result = self.app.scrape_url(
                url,
                formats=["markdown"]
            )

            return result
        except Exception as e:
            print(e)
            return None

    """
        Artikels zoeken met de search functie ipv de scrape functie
        @:return SearchResult met param data, error, ..
    """
    def search_articles(self, query: str, num_results: 10):
        try:
            result = self.app.search(
                query=f"Zoek op de website vrt.be/vrtnws/nl voor nieuws artikels die vandaag gepubliseerd zijn. Een nieuws artikel heeft een titel, inhoud en een schrijver. ",
                limit=num_results,

                # heel veel opties...
                scrape_options=ScrapeOptions(
                    # welk formaat willen we scrapen? markdown is meestal interresanter voor LLMS
                    formats=["markdown"]
                )
            )

            return result
        except Exception as e:
            print(e)
            return None

    """
          prompt=f"On HLN.be's homepage, find the 'Meest gelezen' (most read) section. "
                         "For each listed item, extract the title, URL, a one-sentence summary and if the article is a 'plus' article."
                         f"Only take the first {num_results} items.",

          """
    """
        Artikels ophalen met de extract functie van firecrawl.
        Je geeft obv een prompt aan welke data je wilt opahelen. 
        @:return SearchResult met param data, error, ..
    """
    def extract_articles(self, num_results: int):
        try:
            results = self.app.extract(
                ["https://www.hln.be/binnenland/"],
                prompt=f"On HLN.be's 'NIEUWS' page, find all the articles published today."
                       "For each listed item, extract the title, URL, a one-sentence summary and if the article is a "
                       "'plus' article."
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

    def extract_dummy_articles(self):
        articles = [{'url': 'https://www.hln.be/meer-sport/kijk-daar-sta-je-dan-met-die-auto-van-twee-miljoen-euro-nba-ster-luka-doncic-ontdekt-na-match-onaangename-verrassing~aadc7e60/', 'plus': False, 'title': 'KIJK. Daar sta je dan, met die auto van twee miljoen euro: NBA-ster Luka Doncic ontdekt na match onaangename verrassing', 'summary': 'NBA-ster Luka Doncic ervaart een frustrerende situatie na een oefenmatch met zijn hypercar.'},
                    {'url': 'https://www.hln.be/buitenland/zuidwesten-frankrijk-zet-zich-schrap-voor-hitte-van-buitengewoon-niveau-kwik-stijgt-vlot-boven-40-graden~a4108265/', 'plus': False, 'title': 'Zuidwesten Frankrijk zet zich schrap voor hitte "van buitengewoon niveau": kwik stijgt vlot boven 40 graden', 'summary': 'Zuidwesten Frankrijk bereidt zich voor op extreme hitte met temperaturen die boven de 40 graden stijgen.'},
                    {'url': 'https://www.hln.be/tv/ken-krijgt-klap-in-het-gezicht-van-claudia-in-benb-zoekt-lief-ik-had-eigenlijk-geluk-dat-er-cameras-waren~a2447e7e/', 'plus': False, 'title': 'Ken krijgt klap in het gezicht van Claudia in \'B&B zoekt lief\': "Ik had eigenlijk geluk dat er camera\'s waren"', 'summary': 'In een realityshow krijgt Ken een klap van Claudia, wat leidt tot een onverwachte wending in hun relatie.'},
                    {'url': 'https://www.hln.be/binnenland/de-pablo-escobar-van-de-kempen-tom-bastiaanse-55-de-onopvallende-kempenzoon-die-het-meesterbrein-is-achter-de-grootste-europese-drugsvangst-ooit~afa1e8d5/', 'plus': True, 'title': "'De Pablo Escobar van de Kempen': Tom Bastiaanse (55), de onopvallende Kempenzoon die het meesterbrein is achter de grootste Europese drugsvangst ooit", 'summary': 'Tom Bastiaanse wordt beschuldigd van het leiden van de grootste drugsvangst in Europa.'},
                    {'url': 'https://www.hln.be/bv/kijk-natalia-neemt-haar-kinderen-mee-op-het-podium-de-beste-bezoekers-ooit~aa7ca5e6/', 'plus': False, 'title': 'KIJK. Natalia neemt haar kinderen mee op het podium: "De beste bezoekers ooit"', 'summary': 'Zangeres Natalia deelt een emotioneel moment met haar kinderen tijdens een optreden.'}, {'url': 'https://www.hln.be/houthulst/jonge-vrouw-19-ontsnapt-via-dak-uit-verhakkelde-wagen-na-crash-in-maisveld-in-houthulst~ac04b0e2/', 'plus': False, 'title': 'Jonge vrouw (19) ontsnapt via dak uit verhakkelde wagen na crash in maïsveld in Houthulst', 'summary': 'Een 19-jarige vrouw overleeft een ernstig auto-ongeluk door via het dak van haar auto te ontsnappen.'},
                    {'url': 'https://www.hln.be/binnenland/na-cremerie-koopt-marc-coucke-nu-ook-unieke-collectie-oldtimer-ijskarren-ik-denk-niet-dat-er-in-europa-zo-een-collectie-bestaat-dit-zijn-werkelijk-juweeltjes~a052db52/', 'plus': True, 'title': 'Na crèmerie koopt Marc Coucke nu ook unieke collectie oldtimer ijskarren. "Ik denk niet dat er in Europa zo een collectie bestaat – dit zijn werkelijk juweeltjes"', 'summary': 'Marc Coucke investeert in een unieke collectie van oude ijskarren, die hij als juweeltjes beschouwt.'},
                    {'url': 'https://www.hln.be/binnenland/bedreigde-bouchez-journalist-in-gesprek-over-gehandicaptenkaart-van-chauffeur~a7b0bdd4/', 'plus': True, 'title': 'Bedreigde Bouchez journalist in gesprek over gehandicaptenkaart van chauffeur?', 'summary': 'Politicus Bouchez wordt bedreigd in verband met een gesprek over een gehandicaptenkaart.'}, {'url': 'https://www.hln.be/nieuws/zanger-freek-voelt-zich-heel-goed-longarts-legt-uit-wat-dat-precies-betekent-bij-uitgezaaide-longkanker~ac7d381a/', 'plus': True, 'title': 'Zanger Freek voelt zich "heel goed": longarts legt uit wat dat precies betekent bij uitgezaaide longkanker', 'summary': 'Zanger Freek deelt een positieve update over zijn gezondheidstoestand met betrekking tot longkanker.'}]

        return articles

    def extract_dummy_article_content(self):
        article_content ={'body': 'Zelfs voor NBA-ster Luka Doncic (26) loopt niet altijd alles op wieltjes. Na verlies in een oefenmatch met de Sloveense nationale ploeg kwam hij voor een onprettige verrassing te staan. De deur van zijn hypercar van twee miljoen euro werd geblokkeerd. Daar sta je dan, gefrustreerd, met dat monster van 2.000 pk...\n\nNBA-speler heeft hulp nodig om in luxewagen te stappen\n\nHet NBA-seizoen start pas in oktober, maar Doncic heeft deze zomer een ander doel. Met Slovenië gaat hij binnenkort voor een medaille op het EK basketbal (27 augustus-14 september). Daarbij zal hij in de groepsfase ook onze Belgian Lions tegenkomen, want op 31 augustus is het Slovenië-België in groep D.\n\nTer voorbereiding op dat toernooi speelde Slovenië een oefenpot tegen Duitsland. Lekker liep dat niet: Doncic en co verloren met 89-103.\n\nMaar de grootste uitdaging voor Doncic kwam pas na de wedstrijd. Want toen hij in de ondergrondse parking van de Stožice Arena in hoofdstad Ljubljana zijn peperdure elektrische hypercar opzocht, bleek instappen onmogelijk. Het portier - een vleugeldeur - werd geblokkeerd door een andere wagen.\n\nLicht gefrustreerd nam hij zijn smartphone om hulp te zoeken.\n\nDaar sta je dan, met een auto van twee miljoen euro...\n\nVan de Rimac Nevera, een Kroatische elektrische hypercar, zijn er slechts 150 gemaakt. Met bijna 2.000 pk gaat hij van 0 naar 100 kilometer per uur in 1,74 seconden, en van 0 naar 300 in nog geen tien seconden. De topsnelheid: 412 kilometer per uur. Daarmee is het de snelste elektrische auto op de markt.\n\nAls fanaat van sportwagens móest deze in de collectie van Doncic, die onder meer ook een Apocalypse Hellfire 6x6, Koenigsegg Regera, Brabus Rocket 1000, Lamborghini Urus, Ferrari 812 Superfast en Chevrolet Camaro uit 1968 in de garage heeft staan.\n\nAllemaal betaalbaar, als je een van de topverdieners in de NBA bent. Doncic ondertekende vorige week een nieuw driejarig contract bij de Los Angeles Lakers. Hij zou tot en met 2028 naar verluidt zo’n 142 miljoen euro verdienen.\n\nMaar ook met een gespijsde bankrekening loopt niet altijd alles naar wens.', 'title': 'KIJK. Daar sta je dan, met die auto van twee miljoen euro: NBA-ster Luka Doncic ontdekt na match onaangename verrassing | Meer Sport | hln.be'}

        return article_content['body']

    """
        Bij scrapen weet je de url waar je op wil zoeken
    """

    def scrape_company_pages(self, url: str):
        try:
            result = self.app.scrape_url(
                url,
                formats=["markdown"]
            )
            return result
        except Exception as e:
            print(e)
            return None

    # ----------------
    # Define Firecrawl search tool
    # ----------------
    def search(self, query: str, num_results: int =3):
        try:
            result = self.app.search(
                query=f"{query}",
                limit=num_results
            )

            return result
        except Exception as e:
            print(e)
            return None

