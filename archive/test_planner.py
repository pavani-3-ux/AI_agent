from planner import create_plan, display_plan


# ============================================================
# PLANNER TEST PROGRAM
# ============================================================

print()
print("=" * 65)
print("                    PLANNER TEST")
print("=" * 65)
print()

print("Type 'exit' to stop.")
print()


while True:

    user_input = input(
        "Enter a task: "
    ).strip()


    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    if user_input.lower() in {
        "exit",
        "quit"
    }:

        print()
        print("Planner test finished.")
        break


    # --------------------------------------------------------
    # EMPTY INPUT
    # --------------------------------------------------------

    if not user_input:

        continue


    # --------------------------------------------------------
    # CREATE PLAN
    # --------------------------------------------------------

    print()
    print("Creating plan...")


    plan = create_plan(
        user_input
    )


    # --------------------------------------------------------
    # DISPLAY PLAN
    # --------------------------------------------------------

    display_plan(
        plan
    )