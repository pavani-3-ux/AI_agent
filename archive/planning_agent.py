from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import List


# ============================================================
# LEVEL 6 — PLANNING PHASE
# ============================================================

MODEL_NAME = "qwen3:4b"


# ============================================================
# LLM
# ============================================================

model = ChatOllama(
    model=MODEL_NAME,
    temperature=0
)


# ============================================================
# PLAN STRUCTURE
# ============================================================

class PlanStep(BaseModel):
    step_number: int = Field(
        description="Order of the step"
    )

    action: str = Field(
        description="What should be done"
    )

    tool: str = Field(
        description=(
            "Tool required for this step. "
            "Choose only from: "
            "calculator, get_current_datetime, "
            "unit_converter, search_web, search_pdf, direct"
        )
    )


class TaskPlan(BaseModel):
    planning_required: bool

    reason: str

    steps: List[PlanStep]


# ============================================================
# STRUCTURED PLANNER
# ============================================================

planner = model.with_structured_output(TaskPlan)


# ============================================================
# PLANNING INSTRUCTIONS
# ============================================================

SYSTEM_PROMPT = """
You are the Planning Engine of an AI Agent.

Your ONLY responsibility is to create an execution plan.

You must NOT execute tools.

You must NOT calculate answers.

You must NOT search the internet.

You must NOT search the PDF.

You only analyze the user's request and create
a structured step-by-step plan.

AVAILABLE TOOLS:

calculator
- Mathematical calculations.

get_current_datetime
- Current date and time.

unit_converter
- Unit conversions.

search_web
- Current, recent, latest, live or time-sensitive information.

search_pdf
- Information that must be retrieved from the user's PDF.

direct
- Tasks that require normal LLM processing without a tool.

RULES:

1. Understand the user's actual goal.

2. Decide whether planning is required.

3. Break complex tasks into logical ordered steps.

4. Select the correct tool for every step.

5. Do not create unnecessary steps.

6. A simple task can contain one step.

7. A complex task can contain multiple steps.

8. If current information is requested, use search_web.

9. If information is explicitly requested from the PDF,
   use search_pdf.

10. If calculation is required, use calculator.

11. If date/time is requested, use get_current_datetime.

12. If conversion is required, use unit_converter.

13. If no tool is required, use direct.

14. Do NOT execute any selected tool.

15. The output must be a plan that another component,
    called the Executor, can execute later.
"""


# ============================================================
# CREATE PLAN
# ============================================================

def create_plan(task: str) -> TaskPlan:

    return planner.invoke(
        [
            (
                "system",
                SYSTEM_PROMPT
            ),
            (
                "human",
                task
            )
        ]
    )


# ============================================================
# DISPLAY PLAN
# ============================================================

def show_plan(plan: TaskPlan):

    print()
    print("=" * 65)
    print("                     LEVEL 6 PLAN")
    print("=" * 65)

    print(
        f"Planning Required : {plan.planning_required}"
    )

    print(
        f"Reason            : {plan.reason}"
    )

    print()
    print("Execution Steps:")
    print("-" * 65)

    for step in plan.steps:

        print(
            f"Step {step.step_number}: "
            f"{step.action}"
        )

        print(
            f"        Tool: {step.tool}"
        )

        print()


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 65)
    print("              LEVEL 6 — PLANNING PHASE")
    print("=" * 65)

    print()
    print("Model     : Qwen3:4b")
    print("Runtime   : Ollama")
    print("Framework : LangChain")
    print("Phase     : Planner ONLY")
    print()

    print(
        "The planner creates a plan but does NOT execute it."
    )

    print()
    print("Type 'exit' to stop.")
    print("=" * 65)

    while True:

        try:

            task = input(
                "\nEnter a task: "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError
        ):

            print("\nPlanner stopped.")
            break

        if not task:

            continue

        if task.lower() in {
            "exit",
            "quit",
            "/bye"
        }:

            print("Planner stopped.")
            break

        try:

            print("\nCreating plan...")

            plan = create_plan(task)

            show_plan(plan)

        except Exception as error:

            print()
            print("Planning Error:")
            print(error)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()