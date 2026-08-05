from planning_agent import (
    create_plan,
    show_plan,
)

from executor import execute_plan


print()
print("=" * 65)
print("              LEVEL 6 — PLANNER + EXECUTOR")
print("=" * 65)

print()
print("Planner → Plan → Executor → Tool → Result")
print()

while True:

    task = input(
        "Enter a task: "
    ).strip()

    if not task:
        continue

    if task.lower() in {
        "exit",
        "quit",
        "/bye"
    }:

        print("Goodbye!")
        break

    try:

        # ====================================================
        # PLANNING
        # ====================================================

        print()
        print("Creating plan...")

        plan = create_plan(task)

        show_plan(plan)

        # ====================================================
        # EXECUTION
        # ====================================================

        results = execute_plan(
            plan,
            task
        )

        # ====================================================
        # RESULTS
        # ====================================================

        print()
        print("=" * 65)
        print("                    STEP RESULTS")
        print("=" * 65)

        for result in results:

            print()
            print(
                f"Step {result['step']}"
            )

            print(
                f"Tool: {result['tool']}"
            )

            print(
                f"Action: {result['action']}"
            )

            print()
            print(
                result["result"]
            )

            print("-" * 65)

    except Exception as error:

        print()
        print("LEVEL 6 ERROR:")
        print(error)
        print()