import json
import pprint
import argparse
import itertools
import re

from pprint import pformat


# CSP Problem definition
class CSP:
    def __init__(self, variables: list, domains: list, constraints: list):
        self.variables: list = variables
        self.domains: list = domains
        self.constraints: list = constraints
        self.solution = None

    def solve(self, algorithm):
        assignment = {}
        print(self)
        print("running solver...")
        self.solution = algorithm(
            self.variables, self.domains, self.constraints, assignment
        )
        # print(f"\nresult:: assignment={assignment}")
        return self.solution

    def __str__(self):
        return (
            f"> variables: {self.variables}"
            + f"\n> domains: {self.domains}"
            + f"\n> constraints:\n{pformat(self.constraints,indent=2)}"
            + "\n"
        )


# Backtrack & helper functions
def is_complete(variables: list, assignment: dict):
    len_A = len(assignment)
    len_V = len(variables)
    print(f"  is_complete({assignment})? |A|={len_A} ? |V|={len_V} ({len_A == len_V})")
    return len(assignment) == len(variables)


def select_unassigned_variable(variables: list, domains: dict, assignment: dict):
    unassigned_vars = [var for var in variables if var not in assignment]
    next_var = min(unassigned_vars, key=lambda var: len(domains[var]))
    print(f"  selected {next_var} <- U={unassigned_vars}")
    return next_var


def order_domain_values(var: str, domains: dict, assignment: dict):
    return domains[var]


def contains_one_or_none(clause: list, var, val, assignment: dict):
    # cvalues = clause.values()
    # return all(v in [True, None] for v in cvalues)
    return all(value_of(lit, var, val, assignment) in [True, None] for lit in clause)


def value_of(lit: str, var: str, val: str, assignment: dict):
    bvar = base_var(lit)
    bval = val if bvar == var else assignment.get(bvar, None)
    rval = bval if not is_complement(lit) else not bval
    return rval


def is_consistent(var: str, val: int, constraints: dict, assignment: dict) -> bool:
    """check if var assignment to val is consistent with rest of assignment and constraints"""
    clauses = constraints[var]
    results = [contains_one_or_none(clause, var, val, assignment) for clause in clauses]
    print(f"  any(results): {any(results)} <- {results}")
    return all(results)


def backtrack(variables: list, domains: dict, constraints: dict, assignment: dict):
    print("-" * 40)
    print(f"backtrack(A={assignment})")

    if is_complete(variables, assignment):
        return assignment

    var = select_unassigned_variable(variables, domains, assignment)
    for value in order_domain_values(var, domains, assignment):
        if is_consistent(var, value, constraints, assignment):
            print(f"  assigning {{{var}:{value}}} -> A={assignment}", end=" => ")
            assignment[var] = value
            print(f"{assignment}")

            result = backtrack(variables, domains, constraints, assignment)
            if result is not None:
                return result
            print(f"  removing assignment {var}:{value}")
            del assignment[var]
    return None


# --------------------------------------------------- #


def is_complement(lit: str) -> bool:
    return "'" in lit


def base_var(lit: str) -> str:
    return lit.replace("'", "")


def eval_clause(clause_assignment: dict) -> bool:
    print(f"eval {clause_assignment}")
    if any(val in [1, None] for val in clause_assignment):
        return True
    return False


# ------------------------------------------ #


def output_result(result):
    """output solution to result.json"""
    with open("results.json", "w") as json_fp:
        json.dump(result, json_fp, indent=4)


def var_order(var_set: set[str]) -> list[str]:
    return sorted(list(var_set))  # eg. (v1,v2,...)


def parse_input(input_str: str) -> dict[int, list[str]]:
    """parse input expression into variables"""
    expression = input_str.replace(" ", "")

    lit_pattern = r"(\w+'?)"  # r"(x_\d+'?)"
    clause_pattern = r"\([^()]+\)"

    clauses = re.findall(clause_pattern, expression)
    clauses = {i: re.findall(lit_pattern, clause) for i, clause in enumerate(clauses)}
    return clauses


# cnf_test_expressions = {
#     # test number : (cnf_expr, expected_solution)
#     1 :("(A)", {'A':True}),
#     2 :("(A')", {'A':False}),
#     3 :("(A)(A')", None),
#     4 :("(X+Y)", {'X':True,'Y':True}),
#     5 :("(X+Y')", {'X':True,'Y':True}),
#     6 :("(X'+Y)", {'X':True,'Y':True}),
#     7 :("(X'+Y')", {'X':False,'Y':False}),
#     8 :("(X+Y)(X'+Y)", {'X':True,'Y':True}),
#     9 :("(X+Y)(X'+Y')", {'X':True,'Y':False}),
#     # 10:("(x_1' + x_2)(x_1' + x_3)", {}),
#     # 11:("(x_1' + x_2 + x_4') (x_2 + x_3' + x_4) (x_1 + x_2' + x_3) (x_1 + x_2 + x_3)", {}),
#     # 12:("(x_1' + x_2 + x_4' + x_5') (x_2 + x_3 + x_5' + x_6') (x_1 + x_2 + x_3 + x_5)", {}),
# }

cnf_test_expressions = [
    "(A)",
    "(A')",
    "(A)(A')",
    "(X+Y)",
    "(X+Y')",
    "(X'+Y)",
    "(X'+Y')",
    "(X+Y)(X'+Y)",
    "(X+Y)(X'+Y')",
    "(x_1' + x_2)(x_1' + x_3)",
    "(x_1' + x_2 + x_4') (x_2 + x_3' + x_4) (x_1 + x_2' + x_3) (x_1 + x_2 + x_3)",
    "(x_1' + x_2 + x_4' + x_5') (x_2 + x_3 + x_5' + x_6') (x_1 + x_2 + x_3 + x_5)",
]


def main():
    # input and parse expression data
    for test, cnf_expr in enumerate(cnf_test_expressions):
        input_str = cnf_expr
        print(f'Test {test} :: expression: "{input_str}=1"')
        clause_dict = parse_input(input_str)

        var_set: set[str] = set()
        constraints = {}
        for clause_id, literals in clause_dict.items():
            print(f"  clause {clause_id} literals: [{', '.join(literals)}]")
            for lit in literals:
                bvar = base_var(lit)
                var_set.add(bvar)
                constraints[bvar] = constraints.get(bvar, []) + [literals]
                # print(f"+ constraint (clauses): {constraints}")
        variables = var_order(var_set)

        # set variable domains
        base_domain = (True, False)  # (True,False)
        domains = {var: base_domain for var in var_set}

        # constraints based on clauses
        csp = CSP(variables, domains, constraints)
        solution = csp.solve(backtrack)
        print("-" * 40)
        print(f'solution for expr: "{cnf_expr}=1"\n:: assignment={solution}')
        print("-" * 40)
        print()
        print()


def main_1():
    # input and parse expression data
    input_str = cnf_test_expressions[1]
    input_data = parse_input(input_str)

    # load data into local objects
    expression = input_data["expression"]
    clauses = input_data["clauses"]
    variables = input_data["variables"]
    var_set = set(variables)

    # define domain values
    base_domain = (0, 1)  # (True,False)
    # base_domain = (-1,0,1) # (None,True,False)
    result_dict = {var: -1 for var in var_set}
    domain_dict = {var: base_domain for var in var_set}

    # set up variables, domain, and constraints for csp
    """
    Variable x_i \in X = [x_0,x_1,...,x_n]
    Domain for all x\in X: (F,T) or (0,1)

    \forall a,b \in X:
        where a≠b: a=b' \iff b=a'
    """
    # generate all combinations of hangars,forklifts,times; this is the base domain for all variables

    # generate/construct variable objects
    print()
    print(f"variables: {variables}")
    print(f"domains:\n{pformat(domain_dict,indent=2)}")


main()
