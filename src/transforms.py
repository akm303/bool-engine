"""
Docstring for src.transforms
The Tseytin Transformation takes an arbitrary combinatorial logic circuit
and produces an equisatisfiable boolean formula in CNF form in O(n) ([wiki](https://en.wikipedia.org/wiki/Tseytin_transformation))

output formula grows linearly relative to input circuits
"""

import re
from itertools import count
from typing import Tuple
from common import *


# --------------------------------------------------- #
# type aliases
op_type = str
expr_type = str
subexpr_type = expr_type


# --------------------------------------------------- #
# boolean logic - helper functions


def other_operation(op: op_type) -> op_type | None:
    # operations = {'\\lor':'\\land', '\\land':'\\lor','+':'*','*':'+'}
    operations = {
        "\\lor": "*",  # convert from LaTeX to local syntax
        "\\land": "+",  # convert from LaTeX to local syntax
        "+": "*",
        "*": "+",
    }
    return operations.get(op, None)


def demorgans(x: v_type, op1: op_type, y1: v_type, y2: v_type) -> str:
    """
    applies demorgans on subexpressions in the form `x <op1> (y1 <op2> y2)` where:
     - x,y1,y2 are subexpressions
     - op2 is the opposite logical operation of op1; ie.
        - if op1 = '+', op2 = '*'
        - if op1 = '*', op2 = '+'

    :param x, y1, y2: variables
    :type x, y1, y2: v_type (variable type: str) - variable represents a subexpression
    :param op1: Description
    :type op1: op_type (operation type: str) - operation represented by str
    """
    op2 = other_operation(op1)


def cnf_to_dnf(cnf_expr: str) -> str:
    """
    Docstring for cnf_to_dnf

    :param cnf_expr: a string representing a conjunction of clauses (clause: sums of literals)
    :type cnf_expr: str
    :return: a string representing a disjunction of terms (term: products of literals)
    :rtype: str
    """
    pass


def dnf_to_cnf(dnf_expr: str) -> str:
    """
    Docstring for dnf_to_cnf

    :param dnf_expr: a string representing a disjunction of terms (term: products of literals)
    :type dnf_expr: str
    :return: a string representing a conjunction of clauses (clause: sums of literals)
    :rtype: str
    """
    pass


def fmt_formula(formula_str: str, idt=" " * 2) -> str:
    formula_str = formula_str.replace("\\then", "->")
    formula_str = formula_str.replace("\\iff", "<->")
    formula_str = formula_str.replace("\\land", ".")
    formula_str = formula_str.replace("*", ".")
    formula_str = formula_str.replace("\\lor", "+")

    formula_str = formula_str.replace(" ", "")
    formula_str = formula_str.replace(")(", ").(")

    formula = re.split(r":?=", formula_str)
    target, expression = formula

    # print(f"expression[0,-1] = {expression[0]}, {expression[-1]}")
    if expression[0] != "(" or expression[-1] != ")":
        expression = f"({expression})"

    print(f"{idt}  (lhs,rhs): {target,expression}")
    return target, expression


def parse_formula(
    formula_str: str,
) -> Tuple[e_type, list[v_type], list[l_type], list[c_type]]:

    def var(i):
        return f"X{i}"

    var_count = count()
    subexpr_dict: dict[str, subexpr_type] = {}
    idt = " " * 2  # indent
    subexpr_pattern = r"\([^()]+\)"

    target, expression = fmt_formula(formula_str)
    # print(f'{idt}formatted: "{target}" = "{expression}"')

    i = next(var_count)
    next_var = var(i)
    subexpr_dict[next_var] = ""

    while expression != f"X{i}":
        # add variable per subexpression
        i = next(var_count)
        next_var = var(i)

        subexpr: re.Match = re.search(subexpr_pattern, expression)
        subexpr: str = subexpr.group(0)
        # print(f"{idt*2}replacing subexpr match \"{subexpr}\" with \"{next_var}\"")
        subexpr_dict[next_var] = subexpr.replace(var(i - 1), subexpr_dict[var(i - 1)])

        print(f'{idt}next var: "{next_var}" as "{subexpr}" from "{expression}"')
        print(f'{idt*2}expression: "{expression}"', end=" -> ")
        expression = expression.replace(subexpr, next_var)
        print(f'"{expression}"')

    return subexpr_dict


# --------------------------------------------------- #
def parse_test():
    test_cases = [
        "E = ((p * q) + r) \\then s'",
    ]

    for i, test_formula in enumerate(test_cases):
        print(f'test {i+1}: "{test_formula}"')
        result = parse_formula(test_formula)
        print(f"result: {result}")


def test():
    parse_test()


if __name__ == "__main__":
    test()
