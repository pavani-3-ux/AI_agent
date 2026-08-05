from langchain_ollama import ChatOllama


# ============================================================
# LEVEL 6.5 — FINAL ANSWER GENERATOR
# ============================================================

MODEL_NAME = "qwen3:4b"

model = ChatOllama(
    model=MODEL_NAME,
    temperature=0.2,
)


# ============================================================
# GENERATE FINAL ANSWER
# ============================================================

def generate_final_answer(
    user_query,
    execution_results
):

    # --------------------------------------------------------
    # FORMAT TOOL RESULTS
    # --------------------------------------------------------

    results_text = []

    for item in execution_results:

        results_text.append(
            f"""
Step: {item["step"]}
Tool: {item["tool"]}
Action: {item["action"]}

Result:
{item["result"]}
"""
        )

    combined_results = "\n".join(
        results_text
    )

    # --------------------------------------------------------
    # FINAL ANSWER PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are the final answer generator of an AI Agent.

USER QUERY:
{user_query}

TOOL RESULTS:
{combined_results}

INSTRUCTIONS:

1. Answer the user's exact question.
2. Use the tool results as the primary source.
3. Do not invent information.
4. Do not repeat multiple alternative answers.
5. Give ONE clear and direct answer.
6. Do not show internal tool execution details.
7. Do not mention planner, executor, tools, or internal architecture.
8. If web search results are provided, answer using the relevant
   current information from those results.
9. If PDF/RAG results are provided, answer using the PDF content.
10. If the question is a calculation, provide the final result clearly.
11. If the question asks for current information, do not add
    outdated background information unless it directly answers
    the question.
12. Keep the answer focused on what the user actually asked.

Return ONLY the final answer.
"""

    # --------------------------------------------------------
    # CALL LLM
    # --------------------------------------------------------

    response = model.invoke(
        prompt
    )

    # --------------------------------------------------------
    # EXTRACT TEXT
    # --------------------------------------------------------

    content = response.content

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if "text" in item:

                    text_parts.append(
                        str(item["text"])
                    )

            else:

                text_parts.append(
                    str(item)
                )

        content = "\n".join(
            text_parts
        )

    return str(
        content
    ).strip()