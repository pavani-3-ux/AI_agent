from tools import (
    calculator,
    get_current_datetime,
    unit_converter,
)

from web_search import web_search
from rag_pipeline import search_pdf


# ============================================================
# LEVEL 6 — EXECUTOR
# ============================================================

TOOLS = {
    "calculator": calculator,
    "get_current_datetime": get_current_datetime,
    "unit_converter": unit_converter,
    "search_web": web_search,
    "search_pdf": search_pdf,
}


# ============================================================
# EXECUTE ONE PLAN STEP
# ============================================================

def execute_step(step, original_task):

    tool_name = step.tool

    print()
    print("-" * 65)
    print(f"Executing Step {step.step_number}")
    print(f"Action : {step.action}")
    print(f"Tool   : {tool_name}")
    print("-" * 65)

    # --------------------------------------------------------
    # DIRECT
    # --------------------------------------------------------

    if tool_name == "direct":

        return (
            "This step requires direct processing "
            "by the language model."
        )

    # --------------------------------------------------------
    # CHECK TOOL
    # --------------------------------------------------------

    if tool_name not in TOOLS:

        return f"Unknown tool: {tool_name}"

    tool = TOOLS[tool_name]

    # --------------------------------------------------------
    # EXECUTE TOOL
    # --------------------------------------------------------

    try:

        # ====================================================
        # CALCULATOR
        # ====================================================

        if tool_name == "calculator":

            expression = extract_expression(
                original_task
            )

            return str(
                tool.invoke(expression)
            )

        # ====================================================
        # DATE / TIME
        # ====================================================

        elif tool_name == "get_current_datetime":

            return str(
                tool.invoke({})
            )

        # ====================================================
        # UNIT CONVERTER
        # ====================================================

        elif tool_name == "unit_converter":

            value, from_unit, to_unit = (
                extract_conversion(
                    original_task
                )
            )

            return str(
                tool.invoke(
                    {
                        "value": value,
                        "from_unit": from_unit,
                        "to_unit": to_unit,
                    }
                )
            )

        # ====================================================
        # WEB SEARCH
        # ====================================================

        elif tool_name == "search_web":

            return str(
                tool.invoke(
                    original_task
                )
            )

        # ====================================================
        # PDF RAG
        # ====================================================

        elif tool_name == "search_pdf":

            return str(
                tool.invoke(
                    original_task
                )
            )

        return str(
            tool.invoke(original_task)
        )

    except Exception as error:

        return (
            f"Tool execution failed: {error}"
        )


# ============================================================
# CALCULATOR INPUT EXTRACTION
# ============================================================

def extract_expression(task):

    text = task.lower()

    prefixes = [
        "calculate",
        "compute",
        "solve",
        "what is",
        "find",
    ]

    for prefix in prefixes:

        if text.startswith(prefix):

            text = text[
                len(prefix):
            ].strip()

            break

    allowed = (
        "0123456789"
        "+-*/(). "
    )

    expression = "".join(
        character
        for character in text
        if character in allowed
    )

    if not expression:

        raise ValueError(
            "Could not extract a mathematical expression."
        )

    return expression


# ============================================================
# UNIT CONVERSION EXTRACTION
# ============================================================

def extract_conversion(task):

    import re

    pattern = (
        r"(\d+(?:\.\d+)?)\s*"
        r"([a-zA-Z]+)\s+"
        r"(?:to|in)\s+"
        r"([a-zA-Z]+)"
    )

    match = re.search(
        pattern,
        task
    )

    if not match:

        raise ValueError(
            "Could not understand the unit conversion."
        )

    value = float(
        match.group(1)
    )

    from_unit = match.group(2)

    to_unit = match.group(3)

    return (
        value,
        from_unit,
        to_unit,
    )


# ============================================================
# EXECUTE COMPLETE PLAN
# ============================================================

def execute_plan(
    plan,
    original_task
):

    results = []

    print()
    print("=" * 65)
    print("                    PLAN EXECUTION")
    print("=" * 65)

    for step in plan.steps:

        result = execute_step(
            step,
            original_task
        )

        results.append(
            {
                "step": step.step_number,
                "tool": step.tool,
                "action": step.action,
                "result": result,
            }
        )

        print()
        print("Result:")
        print(result)

    print()
    print("=" * 65)
    print("                 EXECUTION COMPLETE")
    print("=" * 65)

    return results