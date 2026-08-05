from planning_agent import create_plan, show_plan
from executor import execute_plan
from final_answer import generate_final_answer


# ============================================================
# LEVEL 6 — COMPLETE PLANNING AGENT
# ============================================================

print()
print("=" * 70)
print("              LEVEL 6 — PLANNING AI AGENT")
print("=" * 70)

print()
print("Architecture:")
print("User → Planner → Executor → Tools → Final Answer")
print()
print("Available capabilities:")
print("  • Calculator")
print("  • Date & Time")
print("  • Unit Converter")
print("  • Live Web Search")
print("  • PDF RAG")
print("  • Multi-Step Planning")
print()
print("Type 'exit' to stop.")
print("=" * 70)


while True:

    try:

        user_query = input("\nYou: ").strip()

    except (KeyboardInterrupt, EOFError):

        print("\nAgent: Goodbye!")
        break

    if not user_query:
        continue

    if user_query.lower() in {
        "exit",
        "quit",
        "/bye"
    }:

        print("Agent: Goodbye!")
        break

    try:

        # ====================================================
        # STEP 1 — PLANNING
        # ====================================================

        print()
        print("[1/3] Creating plan...")

        plan = create_plan(
            user_query
        )

        show_plan(plan)

        # ====================================================
        # STEP 2 — EXECUTION
        # ====================================================

        print()
        print("[2/3] Executing plan...")

        execution_results = execute_plan(
            plan,
            user_query
        )

        # ====================================================
        # STEP 3 — FINAL ANSWER
        # ====================================================

        print()
        print("[3/3] Generating final answer...")

        final_answer = generate_final_answer(
            user_query,
            execution_results
        )

        # ====================================================
        # DISPLAY
        # ====================================================

        print()
        print("=" * 70)
        print("                       ANSWER")
        print("=" * 70)

        print()
        print(final_answer)

        print()
        print("=" * 70)

    except Exception as error:

        print()
        print("=" * 70)
        print("LEVEL 6 ERROR")
        print("=" * 70)
        print(error)
        print("=" * 70)