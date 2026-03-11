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
    pass

def tseytins():
    pass


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
    assignment_pattern = ASSIGNMENT_PATTERN
    formula_str = formula_str.replace("\\then", "->")
    formula_str = formula_str.replace("\\iff", "<->")
    formula_str = formula_str.replace("\\land", ".")
    formula_str = formula_str.replace("*", ".")
    formula_str = formula_str.replace("\\lor", "+")

    formula_str = formula_str.replace(" ", "")
    formula_str = formula_str.replace(")(", ").(")

    formula = re.split(assignment_pattern, formula_str)
    target, expression = formula

    # print(f"expression[0,-1] = {expression[0]}, {expression[-1]}")
    if expression[0] != "(" or expression[-1] != ")":
        expression = f"({expression})"

    dprint(f"{idt}  (lhs,rhs): {target,expression}")
    return target, expression


def parse_formula(
    formula_str: str,
) -> Tuple[e_type, dict[v_type, e_type]]:

    def get_var(i):
        return f"X{i}"

    idt = " " * 2  # indent
    subexpr_pattern = SUBEXPR_PATTERN
    variable_pattern = TRANSFORM_VARIABLE_PATTERN

    formula = fmt_formula(formula_str)
    # print(f'{idt}formatted: "{target}" = "{expression}"')
    target, expression = formula

    var_count = count()
    subexpr_dict: dict[str, subexpr_type] = {}

    matches = list(re.finditer(subexpr_pattern, expression))
    dprint(f"matches: {matches}")
    replacements = {}
    while matches:
        for match in matches:
            i = next(var_count)
            v = get_var(i)
            sub = match.group(0)

            replacements[sub] = v
            subkey = sub

            subexpr_internal_vars = list(re.finditer(variable_pattern, sub))
            dprint(f"to replace in {sub}: {subexpr_internal_vars}")
            for var_match in subexpr_internal_vars:
                rvar = var_match.group(0)
                sub = sub.replace(rvar, subexpr_dict[rvar])

            subexpr_dict[v] = sub

            dprint(f"{idt*2}i={i}, v={v}, subkey={subkey}, sub={sub}")
            dprint(f"{idt*2}subexpr_dict: {subexpr_dict}")
            dprint(f"{idt*2}replacements: {replacements}")

            dprint(f'{idt*2}expression: "{expression}"', end=" -> ")
            expression = expression.replace(subkey, replacements[subkey])
            dprint(f'"{expression}"')
            dprint()

        # get next set of matches
        matches = list(re.finditer(subexpr_pattern, expression))

    return f"\"{'='.join(formula)}\"", subexpr_dict


# --------------------------------------------------- #
def parse_test():

    test_cases = [
        # --- initial test cases ---
        "F = ((p * q) + r) \\then s'",
        "E=(a+((b+c).(b+d)))",
        "p = ((p * q) + r) \\then s'",
        # --- simple local syntax ---
        "E=(p.q)",
        "R=(p+q)",
        "E=((p+q).r)",
        "E=((p.q)+(r.s))",
        # --- multiple clauses same level ---
        "F=(a+b+c)",
        "F=(a.b.c)",
        "F=((a+b)+(c+d))",
        "F=((a.b).(c.d))",
        # --- nested local syntax ---
        "F=(a+((b+c).(b+d)))",
        "F=((a+b).((c+d).(e+f)))",
        "F=(((a+b).c)+(d.(e+f)))",
        "F=((a.(b+c))+((d+e).f))",
        # --- implication chains ---
        "F=((p.q)->r)",
        "F=(p->(q->r))",
        "F=((p->q)->(r->s))",
        # --- biconditional ---
        "F=(p<->q)",
        "F=((p+q)<->(r+s))",
        # --- full latex syntax ---
        r"F=((p \land q) \lor r)",
        r"F=((p \land q) \then r)",
        r"F=(p \then (q \then r))",
        r"F=((p \lor q) \iff (r \lor s))",
        # --- mixed latex + local ---
        r"F=((p \land q)+r)",
        r"F=((p.q) \lor r)",
        r"F=((p \land q)->(r+s))",
        r"F=((p+q) \then (r.s))",
        # --- deeper mixed nesting ---
        r"F=((a \lor (b+c)).(d \then e))",
        r"F=((a+(b \land c)).((d+e).f))",
    ]

    for i, test_formula in enumerate(test_cases):
        print(bar40)
        print(f"test {i+1:<2}:")
        print(f'          input: "{test_formula}"')
        formula, subexpressions = parse_formula(test_formula)
        print(f"        formula: {formula}")  # formatted formula
        print(f"        subexpr: {subexpressions}")  # dict of subexpressions
        print(bar40)
        print()


def test():
    parse_test()


if __name__ == "__main__":
    args = parse_debug_flag()
    set_debug(args.debug)
    test()
