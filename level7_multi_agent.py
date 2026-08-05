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
# LEVEL 7 / LEVEL 8 OPTIMIZED MULTI-AGENT CORE
# ============================================================

MODEL_NAME = "qwen3:4b"


# ============================================================
# LOCAL LLM
# ============================================================

model = ChatOllama(
    model=MODEL_NAME,
    temperature=0.2,
    think=False,
)


# ============================================================
# HELPER — CLEAN MODEL RESPONSE
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
# WEB AGENT
# ============================================================

def web_agent(query):

    try:

        result = web_search.invoke(query)

        return str(result)

    except Exception as error:

        return f"Web search failed: {error}"


# ============================================================
# RAG AGENT
# ============================================================

def rag_agent(query):

    try:

        result = search_pdf.invoke(query)

        return str(result)

    except Exception as error:

        return f"PDF search failed: {error}"


# ============================================================
# DATE / TIME
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
        "in ",
        " to ",
    ]

    unit_words = [
        "km",
        "kilometer",
        "kilometers",
        "meter",
        "meters",
        "m ",
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
    # CURRENT / RECENT INFORMATION
    # --------------------------------------------------------

    web_keywords = [
        "latest",
        "current",
        "recent",
        "today",
        "right now",
        "this year",
        "this month",
        "news",
        "live",
        "currently",
        "present",
        "who is the current",
        "what is the current",
    ]

    if any(
        keyword in query_lower
        for keyword in web_keywords
    ):

        return "WEB"


    # --------------------------------------------------------
    # DIRECT DATE / TIME
    # --------------------------------------------------------

    if is_datetime_query(query):

        return "DATETIME"


    # --------------------------------------------------------
    # DIRECT UNIT CONVERSION
    # --------------------------------------------------------

    conversion_result = try_unit_conversion(query)

    if conversion_result is not None:

        return "UNIT"


    # --------------------------------------------------------
    # DIRECT CALCULATION
    # --------------------------------------------------------

    calculation_result = try_calculation(query)

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

User question:
{query}

Instructions:

- Answer only the question asked.
- Give one clear answer.
- Be concise.
- Be beginner-friendly.
- Do not mention internal processing.
- Do not mention tools or agents.
- Do not provide unnecessary information.
- Do not invent current or recent information.
"""

    try:

        response = model.invoke(
            prompt
        )

        return clean_response(
            response.content
        )

    except Exception as error:

        return f"Analysis failed: {error}"


# ============================================================
# WEB ANSWER
# ============================================================

def answer_web_question(
    query,
    search_result
):

    prompt = f"""
You are a factual AI assistant.

User question:
{query}

Current web search information:
{search_result}

Instructions:

- Answer ONLY the user's question.
- Give ONE direct answer.
- Use the most recent and relevant information.
- Prefer information that directly answers the query.
- Do not combine old information with current information
  unless necessary.
- Do not invent facts.
- Do not mention the web search.
- Do not mention agents or tools.
- Do not provide unrelated information.
- If the search information does not contain the answer,
  clearly say that the available information is insufficient.

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

        return search_result


# ============================================================
# RAG ANSWER
# ============================================================

def answer_rag_question(
    query,
    pdf_result
):

    prompt = f"""
You are an AI assistant answering questions from a PDF.

User question:
{query}

PDF information:
{pdf_result}

Instructions:

- Answer ONLY from the supplied PDF information.
- Give ONE clear answer.
- Do not invent information.
- Do not use outside knowledge.
- Do not mention agents.
- Do not mention tools.
- Do not mention internal processing.
- If the PDF information does not answer the question,
  say that the information was not found in the PDF.

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

        return pdf_result


# ============================================================
# MAIN AGENT
# ============================================================

def run_agent(query):

    query = query.strip()

    if not query:

        return "Please enter a question."


    # ========================================================
    # ROUTE REQUEST
    # ========================================================

    selected_agent = supervisor(
        query
    )


    # ========================================================
    # DIRECT CALCULATOR
    # ========================================================

    if selected_agent == "CALCULATOR":

        result = try_calculation(
            query
        )

        if result is not None:
            return result

        return "I could not calculate that."


    # ========================================================
    # DIRECT DATE / TIME
    # ========================================================

    if selected_agent == "DATETIME":

        try:

            return str(
                get_current_datetime.invoke({})
            )

        except Exception as error:

            return f"Unable to get the current date and time: {error}"


    # ========================================================
    # DIRECT UNIT CONVERTER
    # ========================================================

    if selected_agent == "UNIT":

        result = try_unit_conversion(
            query
        )

        if result is not None:
            return result

        return "I could not perform that conversion."


    # ========================================================
    # WEB SEARCH
    # ========================================================

    if selected_agent == "WEB":

        search_result = web_agent(
            query
        )

        return answer_web_question(
            query,
            search_result
        )


    # ========================================================
    # PDF RAG
    # ========================================================

    if selected_agent == "RAG":

        pdf_result = rag_agent(
            query
        )

        return answer_rag_question(
            query,
            pdf_result
        )


    # ========================================================
    # GENERAL QUESTION
    # ONE QWEN CALL ONLY
    # ========================================================

    return analysis_agent(
        query
    )


# ============================================================
# OPTIONAL TERMINAL TEST
# ============================================================

def main():

    print()
    print("=" * 60)
    print("             OPTIMIZED LEVEL 7 AI AGENT")
    print("=" * 60)
    print()
    print("Model       : Qwen3:4b")
    print("Thinking    : Disabled")
    print("Web Search  : Tavily")
    print("RAG         : ChromaDB")
    print()
    print("Type 'exit' to stop.")
    print("=" * 60)

    while True:

        try:

            query = input("\nYou: ").strip()

        except (
            KeyboardInterrupt,
            EOFError
        ):

            print("\nAgent: Goodbye!")
            break

        if not query:
            continue

        if query.lower() in {
            "exit",
            "quit",
            "/bye",
        }:

            print("Agent: Goodbye!")
            break

        try:

            answer = run_agent(
                query
            )

            print(
                f"\nAgent: {answer}"
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