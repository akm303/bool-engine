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

# type aliases
e_type = str
c_type = list[int]
v_type = str
l_type = v_type
a_type = dict

# --------------------------------------------------- #
# fill remaining assignment variables with wildcard symbol '*'
# WITH_FILL = False
WITH_FILL = True


def is_complement(literal: l_type) -> bool:
    return "'" in literal


def base_variable(literal: l_type) -> v_type:
    return literal.replace("'", "")


def parse_expression(
    expr_string: str,
) -> Tuple[e_type, list[v_type], list[l_type], list[c_type]]:
    expression = expr_string.replace(" ", "")
    # expression,target = expression.split("=")
    # print(f"expression={expression}")
    # print(f"target={target}")

    lit_pattern = r"(\w+'?)"  # r"(x_\d+'?)"
    clause_pattern = r"\([^()]+\)"

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


# --------------------------------------------------- #


def inverse(val: int) -> int:
    if val is None:
        return None
    return 1 if val == 0 else 0

# def c_str(clause,mode="CNF"):
def c_str(clause):
    """generates a string representing a clause"""
    return f"({f' + '.join(clause)})"

def clist_str(clauses:list[list[v_type]]):
    """generates a string representing a list of clauses"""
    # djunc_delim = ' * '
    djunc_delim = ', '
    # djunc_delim = ' '
    rstr = [c_str(clause) for clause in clauses]
    return f"[{djunc_delim.join(rstr)}]"

def vlist_str(variable_list):
    """generates a string representing a list of variables"""
    return f"[ {f', '.join(variable_list)} ]"

def a_str(assignment:dict):
    """generates a string representing an assignment of boolean values to variables"""
    if not assignment:
        return None
    rstr = [f"{k} : {v}" for k,v in assignment.items()]
    rstr = f"{{ {', '.join(rstr)} }}"
    return rstr

def eval_clause(
    clause: list[l_type], assignment: a_type, indent: str
) -> list[int | None]:
    """returns tuple containing value of clause literals"""
    clause_values = []
    # print(f"{indent}from assignment={assignment}")
    for literal in clause:
        bvar = base_variable(literal)
        bval = assignment.get(bvar, None)
        clause_values.append(bval if bvar == literal else inverse(bval))
    print(f"{indent}? eval clause {c_str(clause)} => {clause_values}")
    return clause_values


def backtrack(
    assignment: a_type,
    variables: list[v_type],
    clauses: list[c_type],
    i_space: int = 0,
) -> a_type[v_type,0|1]:
    indent = " " * i_space
    # print(f"{indent}>> backtrack (A={assignment}, V={variables}, C={clauses})")

    # print(f"{indent}>> backtrack(")
    # print(f"{indent} |   A = {a_str(assignment)},")
    # print(f"{indent} |   V = {vlist_str(variables)},")
    # print(f"{indent} |   C = {clist_str(clauses)},")
    # print(f"{indent} |___)")

    print(f"{indent}>> backtrack ::")
    print(f"{indent} >           :A = {a_str(assignment)}")
    print(f"{indent} >           :V = {vlist_str(variables)}")
    print(f"{indent} >           :C = {clist_str(clauses)}")
    print(f"{indent}>>")


    indent: str = " " * (i_space+2)
    unassigned_vars: list[v_type] = sorted(
        list(set(variables) - set(assignment.keys()))
    )

    if all(1 in eval_clause(c, assignment, indent) for c in clauses):
        # complete assignment, fill remaining var with wildcard and return result
        if WITH_FILL and unassigned_vars:
            for var in unassigned_vars:
                assignment[var] = "*"
        print(f"{indent}solution found! -> A={a_str(assignment)}")
        return assignment

    print(f"{indent}unassigned: U={unassigned_vars}", end=" :: ")
    if unassigned_vars:
        current_var = unassigned_vars.pop(0)
        print(f'-> var="{current_var}"')
        # print(f"{indent}current var: {current_var}")

        assignment[current_var] = 1  # assign(var,1)
        while assignment[current_var] >= 0:
            result = backtrack(assignment, variables, clauses, i_space + 2)
            if result is not None:
                print(f"{indent}<<")
                return result
            assignment[current_var] -= 1

        print(f"{indent}<< no unattempted values; removing {current_var} from assignment",end='')
        del assignment[current_var]

    print(f"\n{indent}<< no unassigned variables; backtracking")
    return None


# --------------------------------------------------- #


def main():
    cnf_test_expressions = [
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
    ]

    for i, cnf_expr in enumerate(cnf_test_expressions):
        print("-" * 40)
        expression, variables, literals, clauses = parse_expression(cnf_expr)
        print(f"expression {i+1}: \"{expression}=1\"")
        print(f"     clauses = {clist_str(clauses)}")
        print(f"    literals = {vlist_str(literals)}")
        print(f"   variables = {vlist_str(variables)}")

        print()
        assignment = a_type()
        result = backtrack(assignment, variables, clauses)
        print()
        print(f"solution: {result}")
        # print(f"solution: {a_str(result)}")

        print("-" * 40)
        print()


if __name__ == "__main__":
    main()
