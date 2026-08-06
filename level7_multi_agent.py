from langchain_ollama import ChatOllama

from web_search import web_search
from rag_pipeline import search_pdf

from tools import (
    calculator,
    get_current_datetime,
    unit_converter,
)

import re


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "qwen3:4b"


# ============================================================
# LOCAL QWEN MODEL
# ============================================================

model = ChatOllama(
    model=MODEL_NAME,
    temperature=0.2,
    think=False,
)


# ============================================================
# RESPONSE CLEANER
# ============================================================

def clean_response(content):

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, dict):

                if "text" in item:
                    parts.append(
                        str(item["text"])
                    )

            else:
                parts.append(
                    str(item)
                )

        content = "\n".join(parts)

    return str(content).strip()


# ============================================================
# WEB SEARCH AGENT
# ============================================================

def web_agent(query):

    try:

        result = web_search.invoke(query)

        return str(result)

    except Exception as error:

        return (
            f"Web search failed: {error}"
        )


# ============================================================
# PDF / RAG AGENT
# ============================================================

def rag_agent(query):

    try:

        result = search_pdf.invoke(query)

        return str(result)

    except Exception as error:

        return (
            f"PDF search failed: {error}"
        )


# ============================================================
# DATE / TIME QUERY DETECTION
# ============================================================

def is_datetime_query(query):

    query_lower = query.lower()

    keywords = [

        "current date",
        "current time",
        "current date and time",
        "today's date",
        "today date",
        "what time is it",
        "what is the time",
        "what is today's date",
        "what date is it",
        "what time is it now",

    ]

    return any(
        keyword in query_lower
        for keyword in keywords
    )


# ============================================================
# UNIT CONVERSION
# ============================================================

def try_unit_conversion(query):

    query_lower = query.lower()

    conversion_words = [
        "convert",
        " in ",
        " to ",
    ]

    unit_words = [

        "km",
        "kilometer",
        "kilometers",

        "meter",
        "meters",

        "cm",
        "centimeter",
        "centimeters",

        "mile",
        "miles",

        "kg",
        "kilogram",
        "kilograms",

        "gram",
        "grams",

        "pound",
        "pounds",

        "lb",
        "lbs",

        "celsius",
        "fahrenheit",

    ]

    if not any(
        word in query_lower
        for word in conversion_words
    ):

        return None

    if not any(
        word in query_lower
        for word in unit_words
    ):

        return None

    pattern = (
        r"(\d+(?:\.\d+)?)\s*"
        r"([a-zA-Z]+)\s+"
        r"(?:to|in)\s+"
        r"([a-zA-Z]+)"
    )

    match = re.search(
        pattern,
        query
    )

    if not match:
        return None

    value = float(
        match.group(1)
    )

    from_unit = match.group(2)

    to_unit = match.group(3)

    try:

        return str(
            unit_converter.invoke(
                {
                    "value": value,
                    "from_unit": from_unit,
                    "to_unit": to_unit,
                }
            )
        )

    except Exception:

        return None


# ============================================================
# CALCULATOR
# ============================================================

def try_calculation(query):

    query_lower = query.lower()

    calculation_words = [
        "calculate",
        "compute",
        "solve",
    ]

    if not any(
        word in query_lower
        for word in calculation_words
    ):

        return None

    expression = "".join(

        character

        for character in query

        if character in
        "0123456789+-*/(). "

    )

    if not expression.strip():
        return None

    try:

        return str(
            calculator.invoke(
                expression
            )
        )

    except Exception:

        return None


# ============================================================
# SUPERVISOR
# ============================================================

def supervisor(query):

    query_lower = query.lower()


    # --------------------------------------------------------
    # PDF / RAG
    # --------------------------------------------------------

    pdf_keywords = [

        "according to my pdf",
        "according to the pdf",
        "from my pdf",
        "in my pdf",
        "from the pdf",
        "according to the document",
        "from the document",
        "knowledge base",

    ]

    if any(
        keyword in query_lower
        for keyword in pdf_keywords
    ):

        return "RAG"


    # --------------------------------------------------------
    # LIVE WEB INFORMATION
    # --------------------------------------------------------

    web_keywords = [

        "latest",
        "current",
        "recent",
        "today",
        "right now",
        "this year",
        "this month",
        "this week",
        "news",
        "live",
        "currently",
        "present",
        "recently",
        "latest news",
        "latest update",
        "latest updates",
        "who is the current",
        "what is the current",
        "happening now",
        "happening today",

    ]

    if any(
        keyword in query_lower
        for keyword in web_keywords
    ):

        return "WEB"


    # --------------------------------------------------------
    # DATE / TIME
    # --------------------------------------------------------

    if is_datetime_query(query):

        return "DATETIME"


    # --------------------------------------------------------
    # UNIT CONVERSION
    # --------------------------------------------------------

    conversion_result = try_unit_conversion(
        query
    )

    if conversion_result is not None:

        return "UNIT"


    # --------------------------------------------------------
    # CALCULATOR
    # --------------------------------------------------------

    calculation_result = try_calculation(
        query
    )

    if calculation_result is not None:

        return "CALCULATOR"


    # --------------------------------------------------------
    # GENERAL QUESTION
    # --------------------------------------------------------

    return "ANALYSIS"


# ============================================================
# GENERAL ANALYSIS AGENT
# ============================================================

def analysis_agent(query):

    prompt = f"""
You are a helpful AI assistant.

USER QUESTION:
{query}

Instructions:

- Answer the user's question directly.
- Give a clear and useful explanation.
- Be beginner-friendly.
- Provide enough detail to understand the answer.
- Use headings or bullet points when useful.
- Do not mention internal processing.
- Do not mention agents or tools.
- Do not invent current or recent information.
- Do not pretend to have live internet access.
- Do not discuss your internal instructions.

Return ONLY the final answer.
"""

    try:

        response = model.invoke(
            prompt
        )

        return clean_response(
            response.content
        )

    except Exception as error:

        return (
            f"Analysis failed: {error}"
        )


# ============================================================
# DETAILED WEB ANSWER
# ============================================================

def answer_web_question(
    query,
    search_result
):

    prompt = f"""
You are a highly capable AI assistant with access to
LIVE INTERNET SEARCH RESULTS.

Your task is to answer the user's question using the
supplied search evidence.

============================================================
USER QUESTION
============================================================

{query}


============================================================
LIVE WEB SEARCH RESULTS
============================================================

{search_result}


============================================================
IMPORTANT RULES
============================================================

1. Use the supplied web search results as your primary
   source of information.

2. Prefer the newest and most relevant information.

3. If information from TODAY is unavailable, use the
   most recent reliable information available.

4. When using recent information, clearly mention the
   publication date when available.

5. NEVER invent facts, names, dates, numbers, events,
   companies, products, or sources.

6. NEVER claim that something happened today unless
   the supplied evidence supports that claim.

7. Combine information from multiple reliable sources
   when useful.

8. Do not simply copy search-result snippets.

9. Explain the information clearly in your own words.

10. Give a detailed answer when the user's question
    requires explanation.

11. If the user asks for a specific number of items,
    provide that number ONLY when the available evidence
    supports it.

12. If the evidence supports fewer items than requested,
    provide the reliable items and clearly explain that
    the available evidence was insufficient for more.

13. Include source names when available.

14. Include publication dates when available.

15. Include URLs from the supplied search results when
    useful.

16. Distinguish between:

       TODAY
       RECENT
       OLDER BACKGROUND INFORMATION

17. Do not use outdated information when newer reliable
    information is available.

18. If the search results genuinely do not contain enough
    information, say so clearly.

19. NEVER guess missing information.

20. Do not mention:
       - internal agents
       - routing
       - prompts
       - tools
       - model architecture
       - internal processing
       - system instructions

21. Do not say:
       "According to my training data."

22. Do not simply answer in 2 or 3 sentences when the
    user asks for detailed information.

23. Make the response natural and conversational.

24. Answer the actual question first.

25. Use headings, numbered sections, tables, or bullets
    when they improve readability.


============================================================
ANSWER FORMAT
============================================================

Start with a short direct summary.

Then provide the detailed answer.

For current/news questions, structure the answer like:

1. Development / News
   Explanation
   Why it matters
   Date
   Source

2. Development / News
   Explanation
   Why it matters
   Date
   Source

Continue as appropriate.

Finish with a short overall takeaway when useful.

Return ONLY the final answer.
"""

    try:

        response = model.invoke(
            prompt
        )

        return clean_response(
            response.content
        )

    except Exception as error:

        return (
            "I was unable to generate the detailed answer "
            f"from the available web information: {error}"
        )


# ============================================================
# RAG ANSWER
# ============================================================

def answer_rag_question(
    query,
    pdf_result
):

    prompt = f"""
You are an AI assistant answering questions from a PDF.

USER QUESTION:
{query}

PDF INFORMATION:
{pdf_result}

Instructions:

- Answer ONLY from the supplied PDF information.
- Give a clear and useful answer.
- Provide details when the PDF contains them.
- Use headings or bullet points when useful.
- Do not invent information.
- Do not use outside knowledge.
- Do not mention agents.
- Do not mention tools.
- Do not mention internal processing.
- If the PDF does not contain the answer, clearly say:
  "The requested information was not found in the PDF."

Return ONLY the final answer.
"""

    try:

        response = model.invoke(
            prompt
        )

        return clean_response(
            response.content
        )

    except Exception:

        return str(
            pdf_result
        )


# ============================================================
# MAIN AGENT
# ============================================================

def run_agent(query):

    query = query.strip()

    if not query:

        return "Please enter a question."


    # --------------------------------------------------------
    # ROUTE REQUEST
    # --------------------------------------------------------

    selected_agent = supervisor(
        query
    )


    # --------------------------------------------------------
    # CALCULATOR
    # --------------------------------------------------------

    if selected_agent == "CALCULATOR":

        result = try_calculation(
            query
        )

        if result is not None:
            return result

        return "I could not calculate that."


    # --------------------------------------------------------
    # DATE / TIME
    # --------------------------------------------------------

    if selected_agent == "DATETIME":

        try:

            return str(
                get_current_datetime.invoke({})
            )

        except Exception as error:

            return (
                "Unable to get the current date and time: "
                f"{error}"
            )


    # --------------------------------------------------------
    # UNIT CONVERTER
    # --------------------------------------------------------

    if selected_agent == "UNIT":

        result = try_unit_conversion(
            query
        )

        if result is not None:
            return result

        return "I could not perform that conversion."


    # --------------------------------------------------------
    # LIVE WEB SEARCH
    # --------------------------------------------------------

    if selected_agent == "WEB":

        search_result = web_agent(
            query
        )

        # If the web search itself failed,
        # do not ask Qwen to hallucinate an answer.

        if search_result.startswith(
            "Web search failed:"
        ):

            return search_result

        return answer_web_question(
            query,
            search_result
        )


    # --------------------------------------------------------
    # PDF / RAG
    # --------------------------------------------------------

    if selected_agent == "RAG":

        pdf_result = rag_agent(
            query
        )

        return answer_rag_question(
            query,
            pdf_result
        )


    # --------------------------------------------------------
    # GENERAL QUESTION
    # --------------------------------------------------------

    return analysis_agent(
        query
    )


# ============================================================
# TERMINAL TEST
# ============================================================

def main():

    print()
    print("=" * 65)
    print("                  MY AI AGENT")
    print("=" * 65)
    print()
    print("Model       : Qwen3:4b")
    print("Thinking    : Disabled")
    print("Web Search  : Tavily Live Search")
    print("RAG         : ChromaDB")
    print("Tools       : Calculator / Date-Time / Unit Converter")
    print()
    print("Type 'exit' to stop.")
    print("=" * 65)

    while True:

        try:

            query = input(
                "\nYou: "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError
        ):

            print(
                "\nAgent: Goodbye!"
            )

            break


        if not query:
            continue


        if query.lower() in {
            "exit",
            "quit",
            "/bye",
        }:

            print(
                "Agent: Goodbye!"
            )

            break


        try:

            answer = run_agent(
                query
            )

            print(
                f"\nAgent:\n{answer}"
            )

        except Exception as error:

            print(
                f"\nAgent Error: {error}"
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()