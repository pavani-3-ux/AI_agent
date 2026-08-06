from ddgs import DDGS
from langchain_core.tools import tool


# ============================================================
# LIVE WEB SEARCH — NO API KEY REQUIRED
# ============================================================

@tool
def web_search(query: str) -> str:
    """
    Search the live internet for current, recent,
    historical, factual, and time-sensitive information.

    Use this tool when the user asks about:
    - current information
    - latest information
    - recent information
    - news
    - current people or positions
    - latest AI models
    - latest technology
    - specific dates or years
    - information that may have changed
    """

    try:
        # ----------------------------------------------------
        # LIVE SEARCH
        # ----------------------------------------------------

        results = DDGS().text(
            query,
            max_results=5
        )

        if not results:
            return (
                "No reliable web results were found "
                "for this query."
            )

        # ----------------------------------------------------
        # BUILD SEARCH EVIDENCE
        # ----------------------------------------------------

        evidence = []

        for index, result in enumerate(results, start=1):

            title = result.get(
                "title",
                "Unknown title"
            )

            body = result.get(
                "body",
                ""
            )

            url = result.get(
                "href",
                ""
            )

            evidence.append(
                f"""
SOURCE {index}

TITLE:
{title}

CONTENT:
{body}

URL:
{url}
"""
            )

        # ----------------------------------------------------
        # RETURN LIVE WEB EVIDENCE
        # ----------------------------------------------------

        return (
            "LIVE WEB SEARCH RESULTS\n\n"
            "The following information was retrieved "
            "from the live internet.\n"
            "Use these results to answer the user's question.\n"
            "Do not invent information.\n\n"
            + "\n".join(evidence)
        )

    except Exception as error:

        return (
            "Web search failed: "
            f"{error}"
        )