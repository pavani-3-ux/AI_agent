from datetime import datetime

from langchain_core.tools import tool


# ============================================================
# TOOL 1 — CALCULATOR
# ============================================================

@tool
def calculator(expression: str) -> str:
    """
    Calculate a basic mathematical expression.

    Use this tool for arithmetic calculations such as:
    25 * 50
    100 + 250
    (100 + 50) * 2
    """

    try:
        allowed_characters = "0123456789+-*/(). "

        if not all(
            character in allowed_characters
            for character in expression
        ):
            return "Invalid mathematical expression."

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception:
        return "I could not calculate that expression."


# ============================================================
# TOOL 2 — CURRENT DATE AND TIME
# ============================================================

@tool
def get_current_datetime() -> str:
    """
    Get the current date and time from the computer
    running the agent.
    """

    current_time = datetime.now()

    return current_time.strftime(
        "%A, %d %B %Y, %I:%M:%S %p"
    )


# ============================================================
# TOOL 3 — UNIT CONVERTER
# ============================================================

@tool
def unit_converter(
    value: float,
    from_unit: str,
    to_unit: str
) -> str:
    """
    Convert common units.

    Supported conversions:

    Length:
    - km to m
    - m to km
    - m to cm
    - cm to m
    - km to miles
    - miles to km

    Weight:
    - kg to g
    - g to kg
    - kg to pounds
    - pounds to kg

    Temperature:
    - celsius to fahrenheit
    - fahrenheit to celsius
    """

    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    # --------------------------------------------------------
    # Length
    # --------------------------------------------------------

    if from_unit == "km" and to_unit == "m":
        result = value * 1000

    elif from_unit == "m" and to_unit == "km":
        result = value / 1000

    elif from_unit == "m" and to_unit == "cm":
        result = value * 100

    elif from_unit == "cm" and to_unit == "m":
        result = value / 100

    elif from_unit == "km" and to_unit in {"mile", "miles"}:
        result = value * 0.621371

    elif from_unit in {"mile", "miles"} and to_unit == "km":
        result = value * 1.60934

    # --------------------------------------------------------
    # Weight
    # --------------------------------------------------------

    elif from_unit == "kg" and to_unit == "g":
        result = value * 1000

    elif from_unit == "g" and to_unit == "kg":
        result = value / 1000

    elif from_unit == "kg" and to_unit in {"pound", "pounds", "lb", "lbs"}:
        result = value * 2.20462

    elif from_unit in {"pound", "pounds", "lb", "lbs"} and to_unit == "kg":
        result = value / 2.20462

    # --------------------------------------------------------
    # Temperature
    # --------------------------------------------------------

    elif from_unit in {"celsius", "c"} and to_unit in {
        "fahrenheit",
        "f"
    }:
        result = (value * 9 / 5) + 32

    elif from_unit in {"fahrenheit", "f"} and to_unit in {
        "celsius",
        "c"
    }:
        result = (value - 32) * 5 / 9

    else:
        return (
            "Unsupported conversion. "
            "Please use a supported unit conversion."
        )

    return f"{value:g} {from_unit} = {result:g} {to_unit}"


# ============================================================
# TOOL TESTING
# ============================================================

if __name__ == "__main__":

    print("Testing Calculator:")
    print(calculator.invoke("25 * 50"))

    print("\nTesting Date/Time:")
    print(get_current_datetime.invoke({}))

    print("\nTesting Unit Converter:")
    print(unit_converter.invoke({
        "value": 5,
        "from_unit": "km",
        "to_unit": "m"
    }))