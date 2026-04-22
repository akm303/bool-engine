"""
convert string representation of boolean expressions/functions across different formats
"""

import re

# --------------------------------------------------- #
def to_syntax(string: str, target_syntax: str):

    target_syntax = target_syntax.lower()
    string = string.replace(" ", "")

    CANON_OR = " OR "
    CANON_AND = " AND "

    # convert to a intermediate canonical form
    string = re.sub(r"(\\lor|\|\||\||\+)", CANON_OR, string)
    string = re.sub(r"(\\land|&&|&|\.)", CANON_AND, string)

    or_op = "+"
    and_op = "."
    if target_syntax in ["latex"]:
        or_op = r"\lor "
        and_op = r"\land "
    elif target_syntax in ["c", "cpp", "c++"]:
        or_op = "||"
        and_op = "&&"
    elif target_syntax in ["py", "python"]:
        or_op = "|"
        and_op = "&"

    string = string.replace(CANON_OR, or_op)
    string = string.replace(CANON_AND, and_op)
    return string


def to_local(string: str) -> str:
    return to_syntax(string, "local")


def to_LaTeX(string: str) -> str:
    return to_syntax(string, "latex")


def to_code(string: str, lang: str) -> str:
    return to_syntax(string, lang)

