"""
Docstring for src.sat

Custom designed and implemented algorithm to solve SAT for expressions in CNF form
input: string expression in CNF
- expression is a disjunction of clauses
- each clause is a conjunction of literals
- each literal is a variable or its complement
output: assignment of boolean variables to evaluate overall expression equal to 1

"""

import re
from pprint import pformat
from typing import Tuple

from common import *

# --------------------------------------------------- #
# fill remaining assignment variables with wildcard symbol '*'
# WITH_FILL = False
WITH_FILL = True

STDOUT_TYPE = 0  # default
# STDOUT_TYPE = 1 #concise


def parse_cnf_expression(
    expr_string: str,
) -> Tuple[e_type, list[v_type], list[l_type], list[c_type]]:
    expression = expr_string.replace(" ", "")

    lit_pattern = LITERAL_PATTERN
    clause_pattern = SUBEXPR_PATTERN

    # clauses: list of clause lists
    # each clause is a list of its literals
    clauses = re.findall(clause_pattern, expression)
    clauses = [re.findall(lit_pattern, clause) for clause in clauses]

    literals: set[l_type] = set()
    variables: set[v_type] = set()
    for clause in clauses:
        for literal in clause:
            literals.add(literal)
            variables.add(base_variable(literal))

    literals = sorted(list(literals))
    variables = sorted(list(variables))

    return expression, variables, literals, clauses


def is_ksat(clauses: list[c_type], k: int) -> bool:
    return all(len(clause) == k for clause in clauses)


def is_2sat(clauses: list[c_type]) -> bool:
    return is_ksat(clauses, 2)


def is_3sat(clauses: list[c_type]) -> bool:
    return is_ksat(clauses, 2)


# --------------------------------------------------- #


def inverse(val: int) -> int:
    if val is None:
        return None
    return 1 if val == 0 else 0


def eval_clause(
    clause: list[l_type], assignment: a_type, indent: str
) -> list[int | None]:
    """returns tuple containing value of clause literals"""
    clause_values = []
    # dprint(f"{indent}from assignment={assignment}")
    for literal in clause:
        bvar = base_variable(literal)
        bval = assignment.get(bvar, None)
        clause_values.append(bval if bvar == literal else inverse(bval))
    dprint(f"{indent}? eval clause {clause_str(clause)} => {clause_values}")
    return clause_values


def is_satisfiable(
    variables: list[v_type],
    clauses: list[c_type],
) -> Tuple[bool, a_type]:
    """returns whether or not an expression is satisfiable, and an assignment as evidence"""
    assignment = a_type()
    assignment = backtrack(assignment, variables, clauses)
    result = bool(assignment)
    return result, assignment


def backtrack(
    assignment: a_type,
    variables: list[v_type],
    clauses: list[c_type],
    i_space: int = 0,
) -> a_type[v_type, 0 | 1]:
    indent = " " * i_space

    if STDOUT_TYPE == 1:
        dprint(f"{indent}>> backtrack (A={assignment}, V={variables}, C={clauses})")
    else:
        dprint(f"{indent}>> backtrack ::")
        dprint(f"{indent} >           :A = {assignment_str(assignment)}")
        dprint(f"{indent} >           :V = {variables_str(variables)}")
        dprint(f"{indent} >           :C = {clauses_str(clauses)}")
        dprint(f"{indent}>>")

    indent: str = " " * (i_space + 2)

    assigned_vars = assignment.keys()
    unassigned_vars: list[v_type] = sorted(list(set(variables) - set(assigned_vars)))

    if all(1 in eval_clause(c, assignment, indent) for c in clauses):
        # complete assignment, fill remaining var with wildcard and return result
        if WITH_FILL and unassigned_vars:
            for var in unassigned_vars:
                assignment[var] = "*"
        dprint(f"{indent}solution found! -> A={assignment_str(assignment)}")
        return assignment

    dprint(f"{indent}unassigned: U={unassigned_vars}", end=" :: ")
    if unassigned_vars:
        current_var = unassigned_vars.pop(0)
        dprint(f'-> var="{current_var}"')
        # dprint(f"{indent}current var: {current_var}")

        assignment[current_var] = 1  # assign(var,1)
        while assignment[current_var] >= 0:
            result = backtrack(assignment, variables, clauses, i_space + 2)
            if result is not None:
                dprint(f"{indent}<<")
                return result
            assignment[current_var] -= 1

        dprint(
            f"{indent}<< no unattempted values; removing {current_var} from assignment",
            end="",
        )
        del assignment[current_var]

    dprint(f"\n{indent}<< no unassigned variables; backtracking")
    return None


# --------------------------------------------------- #


def test():
    cnf_test_expressions = [
        # custom examples
        "(A)",  # 1. {'A':1}
        "(A')",  # 2. {'A':0}
        "(A)(A')",  # 3. None
        "(X+Y)",  # 4. {'X':1,'Y':*}
        "(X+Y')",  # 5. {'X':1,'Y':*}
        "(X'+Y)",  # 6. {'X':1,'Y':1}
        "(X'+Y')",  # 7. {'X':1,'Y':0}
        "(X+Y)(X'+Y)",  # 8. {'X':1,'Y':1}
        "(X+Y)(X'+Y')",  # 9. {'X':1,'Y':0}
        "(x_1' + x_2)(x_1' + x_3)",  # 10. {'x_1':1, 'x_2':1, 'x_3':1}
        "(x_1' + x_2 + x_4') (x_2 + x_3' + x_4) (x_1 + x_2' + x_3) (x_1 + x_2 + x_3)",  # 11. {'x_1':1, 'x_2':1, 'x_3':*, 'x_4':*}
        "(x_1' + x_2' + x_4' + x_5') (x_2' + x_3 + x_5' + x_6') (x_1 + x_2 + x_3 + x_5)",  # 12. {'x_1':1, 'x_2':1, 'x_3':*, 'x_4':*}
        # example form 2SAT on website
        "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1')",
        "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1') (x_3' + x_1)",
        "(x_2' + x_1) (x_1' + x_3) (x_3 + x_1) (x_3' + x_2') (x_3' + x_2)",  # swapped x_1 & x_2
        "(x_a' + x_1) (x_1' + x_3) (x_3 + x_1) (x_3' + x_a') (x_3' + x_a)",  # swapped x_1 & x_3
        # custom examples
        "(x_a' + x_a)",
        "(A + A)(A' + A')",
    ]

    for i, cnf_expr in enumerate(cnf_test_expressions):

        print(bar40)
        expression, variables, literals, clauses = parse_cnf_expression(cnf_expr)
        print(f'expression {i+1}: "{expression}=1"')
        print(f"     clauses = {clauses_str(clauses)}")
        print(f"    literals = {variables_str(literals)}")
        print(f"   variables = {variables_str(variables)}")

        dprint()
        result, assignment = is_satisfiable(variables, clauses)
        result = "is satisfiable" if result is True else "isn't satisfiable"
        print()
        print(f"expression {i+1}: {result}")
        print(f"solution: {assignment_str(assignment)}")
        # dprint(f"solution: {a_str(result)}")

        print(bar40)
        print()


if __name__ == "__main__":
    args = parse_debug_flag()
    set_debug(args.debug)
    test()
