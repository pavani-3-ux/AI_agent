import os

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise RuntimeError(
        "TAVILY_API_KEY is missing from the .env file."
    )


# ============================================================
# TAVILY CLIENT
# ============================================================

client = TavilyClient(
    api_key=TAVILY_API_KEY
)


# ============================================================
# WEB SEARCH TOOL
# ============================================================

@tool
def web_search(query: str) -> str:
    """
    Search the live web for factual, current, recent,
    historical, or time-sensitive information.

    Use this tool when the user asks about:

    - current information
    - latest information
    - recent information
    - historical facts
    - specific years
    - specific dates
    - current people or positions
    - latest AI models
    - latest technology
    - news
    - information that may have changed
    """

    try:

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True,
            include_raw_content=False
        )

        results = response.get(
            "results",
            []
        )

        if not results:
            return (
                "No reliable web results were found "
                "for this query."
            )


        # ----------------------------------------------------
        # BUILD EVIDENCE
        # ----------------------------------------------------

        evidence = []

        for index, result in enumerate(
            results,
            start=1
        ):

            title = result.get(
                "title",
                "Unknown title"
            )

            content = result.get(
                "content",
                ""
            )

            url = result.get(
                "url",
                ""
            )

            published_date = result.get(
                "published_date",
                ""
            )

            evidence.append(
                f"""
SOURCE {index}

TITLE:
{title}

DATE:
{published_date}

CONTENT:
{content}

URL:
{url}
"""
            )


        # ----------------------------------------------------
        # TAVILY SUMMARY
        # ----------------------------------------------------

        answer = response.get(
            "answer",
            ""
        )


        # ----------------------------------------------------
        # FINAL SEARCH OUTPUT
        # ----------------------------------------------------

        output = """
WEB SEARCH EVIDENCE

IMPORTANT:
The information below comes from live web search.

Use the evidence to answer the user's question.
Do not invent information.
Do not contradict reliable evidence using
your internal knowledge.

"""

        if answer:

            output += (
                "SEARCH SUMMARY:\n"
                f"{answer}\n\n"
            )


        output += "\n".join(
            evidence
        )


        return output


    except Exception as error:

        return (
            "Web search failed: "
            f"{error}"
        )