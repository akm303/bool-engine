"""
Docstring for src.transforms
The Tseytin Transformation takes an arbitrary combinatorial logic circuit
and produces an equisatisfiable boolean formula in CNF form in O(n) ([wiki](https://en.wikipedia.org/wiki/Tseytin_transformation))

output formula grows linearly relative to input circuits
"""
import re
from typing import Tuple
from common import *

test_cases = [
    "\\phi = ((p * q) + r) \\then s'",
]


def parse_formula(
    expr_string: str,
) -> Tuple[e_type, list[v_type], list[l_type], list[c_type]]:
    expression = expr_string.replace(" ", "")

    lit_pattern = r"(\w+'?)"  # r"(x_\d+'?)"
    clause_pattern = r"\([^()]+\)"

    subexpressions = re.findall(clause_pattern, expression)
    subexpressions = [re.findall(lit_pattern, subexpr) for subexpr in subexpressions]

    literals: set[l_type] = set()
    variables: set[v_type] = set()
    for subexpr in subexpressions:
        for literal in subexpr:
            literals.add(literal)
            variables.add(base_variable(literal))

    literals = sorted(list(literals))
    variables = sorted(list(variables))

    return expression, variables, literals, subexpressions