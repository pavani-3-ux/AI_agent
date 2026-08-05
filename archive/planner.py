import json

from langchain_ollama import ChatOllama


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "qwen3:4b"


# ============================================================
# INITIALIZE PLANNER MODEL
# ============================================================

planner_model = ChatOllama(
    model=MODEL_NAME,
    temperature=0
)


# ============================================================
# PLANNER PROMPT
# ============================================================

PLANNER_PROMPT = """
You are the Planning Engine of an AI Agent.

Your job is ONLY to analyze the user's request and create
a logical execution plan.

You must NOT execute the task.
You must NOT answer the user's question.
You must ONLY create the plan.

AVAILABLE TOOLS:

1. calculator
Use for mathematical calculations.

2. get_current_datetime
Use for current date and time.

3. unit_converter
Use for unit conversions.

4. web_search
Use for current, recent, latest, historical, or
time-sensitive information from the internet.

5. search_pdf
Use for information contained inside the AI Fundamentals PDF.

6. direct
Use when no external tool is required and the LLM can
handle the step directly.

============================================================
PLANNING RULES
============================================================

RULE 1:
If the request is simple, create only one step.

RULE 2:
If the request requires multiple actions, break it into
multiple logical steps.

RULE 3:
Use only the tools listed above.

RULE 4:
Do not invent tools.

RULE 5:
Steps must be ordered logically.

RULE 6:
If one step depends on the result of another step,
place the first step before the dependent step.

RULE 7:
For current or recent information, use web_search.

RULE 8:
For information specifically requested from the PDF,
use search_pdf.

RULE 9:
Do not use web_search for simple questions that do not
need current information.

RULE 10:
Do not use search_pdf unless the PDF is relevant.

============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

Do not use markdown.

Do not add explanations outside the JSON.

Use exactly this structure:

{
    "needs_planning": true,
    "reason": "short explanation",
    "steps": [
        {
            "step": 1,
            "action": "what needs to be done",
            "tool": "tool_name"
        }
    ]
}

============================================================
IMPORTANT
============================================================

The tool field must be one of:

calculator
get_current_datetime
unit_converter
web_search
search_pdf
direct
"""


# ============================================================
# CREATE PLAN
# ============================================================

def create_plan(user_request: str):

    prompt = f"""
{PLANNER_PROMPT}

USER REQUEST:
{user_request}
"""

    try:

        response = planner_model.invoke(prompt)

        content = response.content


        # ----------------------------------------------------
        # Handle structured response
        # ----------------------------------------------------

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


        content = str(content).strip()


        # ----------------------------------------------------
        # Remove markdown code fences if model adds them
        # ----------------------------------------------------

        if content.startswith("```"):

            lines = content.splitlines()

            lines = lines[1:]

            if lines and lines[-1].strip() == "```":

                lines = lines[:-1]

            content = "\n".join(lines).strip()


        # ----------------------------------------------------
        # Parse JSON
        # ----------------------------------------------------

        plan = json.loads(content)


        # ----------------------------------------------------
        # Basic validation
        # ----------------------------------------------------

        if not isinstance(plan, dict):

            raise ValueError(
                "Planner returned invalid data."
            )


        if "steps" not in plan:

            raise ValueError(
                "Planner response does not contain steps."
            )


        if not isinstance(
            plan["steps"],
            list
        ):

            raise ValueError(
                "Planner steps must be a list."
            )


        # ----------------------------------------------------
        # Validate tools
        # ----------------------------------------------------

        allowed_tools = {
            "calculator",
            "get_current_datetime",
            "unit_converter",
            "web_search",
            "search_pdf",
            "direct"
        }


        for step in plan["steps"]:

            tool_name = step.get(
                "tool",
                "direct"
            )

            if tool_name not in allowed_tools:

                step["tool"] = "direct"


        return plan


    except Exception as error:

        # ----------------------------------------------------
        # Safe fallback
        # ----------------------------------------------------

        return {
            "needs_planning": False,

            "reason": (
                "Planner could not create a structured plan."
            ),

            "steps": [
                {
                    "step": 1,
                    "action": user_request,
                    "tool": "direct"
                }
            ],

            "error": str(error)
        }


# ============================================================
# DISPLAY PLAN
# ============================================================

def display_plan(plan):

    print()
    print("=" * 65)
    print("                         TASK PLAN")
    print("=" * 65)


    print(
        f"Planning required: "
        f"{plan.get('needs_planning', False)}"
    )


    reason = plan.get(
        "reason",
        ""
    )

    if reason:

        print(
            f"Reason: {reason}"
        )


    print()
    print("Steps:")
    print()


    steps = plan.get(
        "steps",
        []
    )


    if not steps:

        print("No steps generated.")

    else:

        for step in steps:

            number = step.get(
                "step",
                "?"
            )

            action = step.get(
                "action",
                ""
            )

            tool = step.get(
                "tool",
                "direct"
            )


            print(
                f"Step {number}: {action}"
            )

            print(
                f"         Tool: {tool}"
            )

            print()


    print("=" * 65)
    print()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 65)
    print("                  AI AGENT PLANNER")
    print("=" * 65)
    print()

    user_request = input(
        "Enter a task: "
    ).strip()


    if user_request:

        print()
        print("Creating plan...")

        plan = create_plan(
            user_request
        )

        display_plan(
            plan
        )