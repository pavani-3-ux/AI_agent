from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from tools import (
    calculator,
    get_current_datetime,
    unit_converter,
)

from web_search import web_search
from rag_pipeline import search_pdf

from memory import (
    initialize_database,
    save_memory,
    load_memories,
)


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "qwen3:4b"


# ============================================================
# INITIALIZE LOCAL LLM
# ============================================================

model = ChatOllama(
    model=MODEL_NAME,
    temperature=0.2,
)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a helpful, accurate AI Agent.

You have access to several tools, INCLUDING LIVE INTERNET ACCESS via the web_search tool.
Do NOT claim you cannot access the internet. NEVER simulate, guess, or invent data.

Your most important responsibility is to give ONE
clear answer that directly answers the user's question.

============================================================
WEB SEARCH RULE
============================================================

Use web_search whenever the question involves:

- current information
- latest information
- recent events
- a specific year
- a specific date
- current office holders
- historical facts that should be verified
- latest AI models
- latest technology
- news
- information that may have changed

Examples:

"Who is the Prime Minister of India?"

"What is the latest DeepSeek model?"

"Who was the Prime Minister of India in 2024?"

"What happened in AI this week?"

============================================================
WEB EVIDENCE RULE
============================================================

When web_search is used:

1. Treat the retrieved web evidence as the primary source.

2. Answer the user's exact question.

3. Do NOT mix conflicting information from your
   internal model knowledge with the retrieved evidence.

4. Do NOT guess.

5. Do NOT invent dates, names, events, or facts.

6. If reliable evidence clearly answers the question,
   give that answer directly.

7. If the question asks about a particular year,
   answer specifically for that year.

8. Do not replace a historical answer with the
   present-day answer unless the user asks for both.

9. Do not provide unrelated information.

10. Give ONE coherent answer.

============================================================
ANSWER STYLE
============================================================

The user wants direct answers.

Do NOT produce:

- emojis, markdown tables, bullet points, or dividers (---)
- multiple conflicting answers
- unnecessary historical background
- unrelated current information
- repeated explanations
- speculation
- internal reasoning
- simulated or fake data

Your final answer MUST be extremely concise (1 to 2 sentences maximum).

Example:

User:
"Who was the Prime Minister of India in 2024?"

Good answer:

"Narendra Modi was the Prime Minister of India in 2024. He began his third consecutive term on 9 June 2024."

============================================================
RAG RULE
============================================================

Use search_pdf when the user explicitly asks about
information contained in the PDF.

When using RAG:

- use the retrieved PDF information
- answer the question directly
- do not invent information
- do not mix unrelated web information

============================================================
CALCULATOR RULE
============================================================

Use calculator for mathematical calculations.

============================================================
DATE/TIME RULE
============================================================

Use get_current_datetime for the actual current
date and time.

============================================================
UNIT CONVERSION RULE
============================================================

Use unit_converter for supported conversions.

============================================================
MULTI-STEP RULE
============================================================

For complex questions, multiple tools may be used.

Example:

"Find the latest DeepSeek model and compare it
with the AI concepts in my PDF."

Workflow:

1. Search current DeepSeek information.
2. Search the PDF.
3. Compare the retrieved information.
4. Give ONE final answer.

Do not expose internal reasoning.

============================================================
FINAL RULE
============================================================

Always answer the user's actual question.

Give ONE clear final answer.

Never give two contradictory answers.
"""


# ============================================================
# TOOLS
# ============================================================

TOOLS = [
    calculator,
    get_current_datetime,
    unit_converter,
    web_search,
    search_pdf,
]


# ============================================================
# CREATE AI AGENT
# ============================================================

agent = create_agent(
    model=model,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
)


# ============================================================
# INITIALIZE MEMORY DATABASE
# ============================================================

initialize_database()


# ============================================================
# LOAD PREVIOUS MEMORY
# ============================================================

conversation_history = load_memories()


# ============================================================
# HEADER
# ============================================================

print()
print("=" * 65)
print("                 MY AI AGENT - LEVEL 6")
print("=" * 65)
print()

print("Model       : Qwen3:4b")
print("Runtime     : Ollama")
print("Framework   : LangChain")
print("Memory      : SQLite")
print("Web Search  : Tavily")
print("RAG         : ChromaDB")
print()

print("Capabilities:")
print("  1. Calculator")
print("  2. Date & Time")
print("  3. Unit Converter")
print("  4. Live Web Search")
print("  5. PDF RAG")
print("  6. Persistent Memory")
print("  7. Multi-Step Planning")
print()

print("Type 'exit', 'quit', or '/bye' to stop.")
print("=" * 65)
print()


# ============================================================
# MEMORY STATUS
# ============================================================

if conversation_history:

    print(
        f"Previous conversation memory loaded: "
        f"{len(conversation_history)} messages"
    )

else:

    print("No previous conversation memory found.")

print()


# ============================================================
# MAIN LOOP
# ============================================================

