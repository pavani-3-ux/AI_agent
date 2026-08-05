from planner import create_plan, display_plan
from executor import execute_plan, display_results


print()
print("=" * 65)
print("              LEVEL 6.2 PLANNER + EXECUTOR")
print("=" * 65)
print()

user_request = input(
    "Enter a task: "
).strip()


if not user_request:

    print(
        "No task entered."
    )

    exit()


# ============================================================
# CREATE PLAN
# ============================================================

print()
print("Creating plan...")

plan = create_plan(
    user_request
)


display_plan(
    plan
)


# ============================================================
# EXECUTE PLAN
# ============================================================

results = execute_plan(
    plan,
    user_request
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

display_results(
    results
)