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
                """

    # Nieuws samenvatter

    NEWS_FACT_CHECKER_ASSISTANT="""
                                    Je bent een journalist met jaren ervaring en enorme hoeveelheid kennis.
                                    Jouw taak is om artikels na te lezen en kijken of ze feitelijk kloppen.
                                """

    @staticmethod
    def news_fact_checker_user(content: str) -> str:
        return f"""
                        Ga na indien het volgende artikel feitelijk juist is. Geef ook aan waarom wel of niet. 
                        
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
    @staticmethod
    def tool_extraction_user(query: str, content: str) -> str:
        return f"""Query: {query}
                Article Content: {content}

                Extract a list of specific tool/service names mentioned in this content that are relevant to "{query}".

                Rules:
                - Only include actual product names, not generic terms
                - Focus on tools developers can directly use/implement
                - Include both open source and commercial options
                - Limit to the 5 most relevant tools
                - Return just the tool names, one per line, no descriptions

                Example format:
                Supabase
                PlanetScale
                Railway
                Appwrite
                Nhost"""

    # Company/Tool analysis prompts
    TOOL_ANALYSIS_SYSTEM = """You are analyzing developer tools and programming technologies. 
                            Focus on extracting information relevant to programmers and software developers. 
                            Pay special attention to programming languages, frameworks, APIs, SDKs, and development workflows."""

    @staticmethod
    def tool_analysis_user(company_name: str, content: str) -> str:
        return f"""Company/Tool: {company_name}
                Website Content: {content[:2500]}

                Analyze this content from a developer's perspective and provide:
                - pricing_model: One of "Free", "Freemium", "Paid", "Enterprise", or "Unknown"
                - is_open_source: true if open source, false if proprietary, null if unclear
                - tech_stack: List of programming languages, frameworks, databases, APIs, or technologies supported/used
                - description: Brief 1-sentence description focusing on what this tool does for developers
                - api_available: true if REST API, GraphQL, SDK, or programmatic access is mentioned
                - language_support: List of programming languages explicitly supported (e.g., Python, JavaScript, Go, etc.)
                - integration_capabilities: List of tools/platforms it integrates with (e.g., GitHub, VS Code, Docker, AWS, etc.)

                Focus on developer-relevant features like APIs, SDKs, language support, integrations, and development workflows."""

    # Recommendation prompts
    RECOMMENDATIONS_SYSTEM = """You are a senior software engineer providing quick, concise tech recommendations. 
                            Keep responses brief and actionable - maximum 3-4 sentences total."""

    @staticmethod
    def recommendations_user(query: str, company_data: str) -> str:
        return f"""Developer Query: {query}
                Tools/Technologies Analyzed: {company_data}

                Provide a brief recommendation (3-4 sentences max) covering:
                - Which tool is best and why
                - Key cost/pricing consideration
                - Main technical advantage

                Be concise and direct - no long explanations needed."""