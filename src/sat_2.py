import re
from pprint import pformat
from typing import Tuple

expr_type = str
clause_type = list[int]
var_type = str
lit_type = var_type
assignment_type = dict

# --------------------------------------------------- #
# fill remaining assignment variables with wildcard symbol '*'
WITH_FILL = False


def is_complement(literal: lit_type):
    return "'" in literal


def base_variable(literal: lit_type):
    return literal.replace("'", "")


def parse_expression(
    expr_string: str,
) -> Tuple[expr_type, list[var_type], list[lit_type], list[clause_type]]:
    expression = expr_string.replace(" ", "")

    lit_pattern = r"(\w+'?)"  # r"(x_\d+'?)"
    clause_pattern = r"\([^()]+\)"

    clauses = re.findall(clause_pattern, expression)
    clauses = [re.findall(lit_pattern, clause) for clause in clauses]

    literals = set()
    variables = set()
    for clause in clauses:
        for literal in clause:
            literals.add(literal)
            variables.add(base_variable(literal))

    literals = sorted(list(literals))
    variables = sorted(list(variables))

    return expression, variables, literals, clauses


# --------------------------------------------------- #


def other(val: int) -> int:
    return 1 if val == 0 else 0


def eval_clause(
    clause: list[lit_type], assignment: assignment_type, indent_space
) -> list[int | None]:
    """returns tuple containing value of clause literals"""
    clause_values = []
    for literal in clause:
        bvar = base_variable(literal)
        bval = assignment.get(bvar, None)
        clause_values.append(bval if bvar == literal else other(bval))
    print(
        f"{indent_space}? eval clause: {clause} from assignment={assignment} => {clause}={clause_values}"
    )
    return clause_values


def backtrack(
    assignment: assignment_type,
    variables: list[var_type],
    clauses: list[clause_type],
    indent=2,
):
    print(f"{' '*(indent-2)}>> backtrack(A={assignment},V={variables},C={clauses})")
    pindent = " " * indent

    unassigned_vars = sorted(list(set(variables) - set(assignment.keys())))
    if all(1 in eval_clause(c, assignment, pindent) for c in clauses):
        # complete assignment, fill remaining var with wildcard and return result
        if WITH_FILL and unassigned_vars:
            for var in unassigned_vars:
                assignment[var] = "*"
        print(f"{pindent}solution found! -> A={assignment}")
        return assignment

    print(f"{pindent}unassigned: U={unassigned_vars}")
    if not unassigned_vars:
        print(f"{pindent}no unassigned variables; backtracking")
        return None

    current_var = unassigned_vars.pop(0)
    print(f"{pindent}current var: {current_var}")

    assignment[current_var] = 1  # assign(var,1)
    while assignment[current_var] >= 0:
        result = backtrack(assignment, variables, clauses, indent + 2)
        if result is not None:
            return result
        assignment[current_var] -= 1

    print(f"{pindent}no unattempted values; backtracking")
    return None


# --------------------------------------------------- #


def main():
    cnf_test_expressions = [
        "(A)",  # 1. {'A':True}
        "(A')",  # 2. {'A':False}
        "(A)(A')",  # 3. None
        "(X+Y)",  # 4. {'X':True,'Y':*}
        "(X+Y')",  # 5. {'X':True,'Y':*}
        "(X'+Y)",  # 6. {'X':*,'Y':True}
        "(X'+Y')",  # 7. {'X':*,'Y':False}
        "(X+Y)(X'+Y)",  # 8. {'X':True,'Y':True}
        "(X+Y)(X'+Y')",  # 9. {'X':True,'Y':False}
        "(x_1' + x_2)(x_1' + x_3)",
        "(x_1' + x_2 + x_4') (x_2 + x_3' + x_4) (x_1 + x_2' + x_3) (x_1 + x_2 + x_3)",
        "(x_1' + x_2 + x_4' + x_5') (x_2 + x_3 + x_5' + x_6') (x_1 + x_2 + x_3 + x_5)",
    ]

    for cnf_expr in cnf_test_expressions:
        print("-" * 40)
        expression, variables, literals, clauses = parse_expression(cnf_expr)
        print(f"expression: {expression}=1")
        print(f"clauses:\n{pformat(clauses)}")
        print(f" literals: {literals}")
        print(f"variables: {variables}")
        assignment = assignment_type()

        print()
        print(f"init assignment: {assignment}")
        result = backtrack(assignment, variables, clauses)
        print()
        print(f"solution: {result}")

        print("-" * 40)
        print()


if __name__ == "__main__":
    main()
