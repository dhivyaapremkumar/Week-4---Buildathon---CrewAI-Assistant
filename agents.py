import os
from dotenv import load_dotenv

from crewai import Agent, LLM
from crewai.tools import tool
from serpapi import GoogleSearch

# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# -----------------------------
# LLM Configuration
# -----------------------------

llm = LLM(
    model="gpt-4.1-mini",
    api_key=OPENAI_API_KEY,
    temperature=0.3
)

# -----------------------------
# SerpAPI Search Tool
# -----------------------------

@tool("Google Search Tool")
def google_search(query: str) -> str:
    """
    Searches Google using SerpAPI and returns the top search results.
    """

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": 5
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "organic_results" not in results:
        return "No search results found."

    output = ""

    for idx, item in enumerate(results["organic_results"], start=1):
        output += (
            f"{idx}. {item.get('title', '')}\n"
            f"{item.get('snippet', '')}\n"
            f"{item.get('link', '')}\n\n"
        )

    return output
# -----------------------------
# Greeting Agent
# -----------------------------

greeting_agent = Agent(
    role="Greeting Specialist",
    goal="Welcome the user professionally and acknowledge their request before handing it over to the Search Agent.",
    backstory="""
    You are the first point of contact in the AI assistant.
    Your responsibility is to greet users warmly, acknowledge their query,
    and inform them that the Search Agent is searching the web.
    Never answer the user's question yourself.
    Keep your response friendly, concise, and professional.
    """,
    llm=llm,
    verbose=True,
    allow_delegation=False
)
# -----------------------------
# Search Agent
# -----------------------------

search_agent = Agent(
    role="Web Research Specialist",
    goal="Search the web and provide accurate, concise, and up-to-date information to answer the user's query.",
    backstory="""
    You are an expert Web Research Specialist.

Always use the Google Search Tool.

Return your response in Markdown.

Use this format:

# Summary

...

## Key Findings

- Point 1

- Point 2

## Sources

- Source 1

- Source 2
    """,
    llm=llm,
    tools=[google_search],
    verbose=True,
    allow_delegation=False
)
# -----------------------------
# Logger Agent
# -----------------------------

logger_agent = Agent(
    role="Execution Logger",

    goal="""
    Create a professional execution log using the outputs
    from the Greeting Agent and Search Agent.
    """,

    backstory="""
    You are responsible for documenting the execution.

    You do not greet users.

    You do not perform web searches.

    Your only responsibility is to organize the outputs
    from previous agents into a clean, readable report.
    """,

    llm=llm,

    verbose=True,

    allow_delegation=False
)