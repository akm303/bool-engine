"""
Docstring for src.common

type definitions, constants, and functions common across project
"""

import re

# --------------------------------------------------- #
# type aliases
e_type = str  # e = expression
c_type = list[int]  # c = clause
v_type = str  # v = variable
l_type = v_type  # l = literal


# regex patterns
SUBEXPR_PATTERN = r"\([^()]+\)"
LITERAL_PATTERN = r"(\w+'?)"  # r"(x_\d+'?)"
# SATSOLVER_VARIABLE_PATTERN = r"(\w+)'?"  # r"(x_\d+'?)" #todo: test
TRANSFORM_VARIABLE_PATTERN = r"X\d+"
ASSIGNMENT_PATTERN = r":?="

# --------------------------------------------------- #
# debug print
DEBUG_PRINT = False


# DEBUG_PRINT = True
def dprint(*args, **kwargs):
    if DEBUG_PRINT:
        print(*args, **kwargs)


# --------------------------------------------------- #
# string formatting
def bar(n):
    return "-" * n


bar40 = bar(40)


def c_str(clause):
    """generates a string representing a clause"""
    return f"({f' + '.join(clause)})"


def clist_str(clauses: list[list[v_type]]):
    """generates a string representing a list of clauses"""
    # djunc_delim = ' * '
    djunc_delim = ", "
    # djunc_delim = ' '
    rstr = [c_str(clause) for clause in clauses]
    return f"[{djunc_delim.join(rstr)}]"


def vlist_str(variable_list):
    """generates a string representing a list of variables"""
    return f"[ {f', '.join(variable_list)} ]"


def a_str(assignment: dict):
    """generates a string representing an assignment of boolean values to variables"""
    if not assignment:
        return None
    rstr = [f"{k} : {v}" for k, v in assignment.items()]
    rstr = f"{{ {', '.join(rstr)} }}"
    return rstr


# def to_LaTeX(string: e_type):
#     variables = string.match()
#     for varstr in list(variables):
#         string.replace(
#             r"\w+'?", rf"\\neg{varstr}"
#     )


# --------------------------------------------------- #
# common boolean-logic helpers


def is_complement(literal: l_type) -> bool:
    return "'" in literal


def base_variable(literal: l_type) -> v_type:
    return literal.replace("'", "")
