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
        print(f"variables: {self.variables}")
        print(f"domains: {self.domains}")
        print(f"constraints:\n{pformat(self.constraints)}")
        print()
        self.solution = algorithm(
            self.variables, self.domains, self.constraints, assignment
        )
        print(f"\nresulting assignment: {assignment}")
        return self.solution


# Backtrack & helper functions
def is_complete(variables: list, assignment: dict):
    len_A = len(assignment)
    len_V = len(variables)
    print(f"\nis_complete({assignment})? |A|={len_A} ? |V|={len_V} ({len_A == len_V})")
    return len(assignment) == len(variables)


def select_unassigned_variable(variables: list, domains: dict, assignment: dict):
    unassigned_vars = [var for var in variables if var not in assignment]
    next_var = min(unassigned_vars, key=lambda var: len(domains[var]))
    print(f"selected {next_var} <- U={unassigned_vars}")
    return next_var


def order_domain_values(var: str, domains: dict, assignment: dict):
    return domains[var]


def is_consistent(var: str, val: int, constraints: dict, assignment: dict) -> bool:
    print(f"\nis_consistent({assignment}) with {{{var}:{val}}}")
    clauses = constraints[var]
    for clause in clauses:
        print("gathering assignment...")
        clause_assignment = {literal: get_value(literal, var, val, assignment) for literal in clause}
        # clause_assignment = [value(var, val, cvar, assignment) for cvar in clause]
        print(f"  eval(clause={clause}, A={assignment}+{{{var}:{val}}}) => Clause_Assignment={clause_assignment}")
        # clause_result = evaluate_clause(clause_assignment)

        clause_result = eval_clause(clause_assignment)
        print(f"  clause result: {clause_result}")

        # if any(clause_assignment):
        #     print(f"    any({clause_assignment})==True")
        #     continue
        # else:
        #     print(f"    any({clause_assignment})==True")
        #     return False
    return True


def backtrack(variables: list, domains: dict, constraints: dict, assignment: dict):
    print("-" * 40)
    print(f"backtrack(assignment) -> {assignment}")
    if is_complete(variables, assignment):
        return assignment

    var = select_unassigned_variable(variables, domains, assignment)
    for value in order_domain_values(var, domains, assignment):
        if is_consistent(var, value, constraints, assignment):
            print(f"assigning {var}:{value} in {assignment}", end=" => ")
            assignment[var] = value
            print(f"{assignment}")

            result = backtrack(variables, domains, constraints, assignment)
            if result is not None:
                return result
            print(f"removing assignment {var}:{value}")
            del assignment[var]
    return None


# --------------------------------------------------- #


def output_result(result):
    """output solution to result.json"""
    with open("results.json", "w") as json_fp:
        json.dump(result, json_fp, indent=4)


def order(var_set: set[str]) -> list[str]:
    return sorted(list(var_set))  # eg. (v1,v2,...)


def is_complement(var: str) -> bool:
    return "'" in var


def complement(lit: str) -> str:
    return lit[:-1] if is_complement(lit) else lit + "'"


def base_var(lit: str) -> str:
    return lit if not is_complement(lit) else lit[:-1]


def get_value(literal:str, var:str, val:bool, assignment: dict):
    """get value of the literal based on either the assignment or trial variable"""

    print(f"  get value(lit={literal:2}, (var={var}, val={val}, A={assignment})) from", end=" ")
    bvar = base_var(literal)
    if bvar == var:
        print(f"trial (lit={literal} -> {var}) with {{{var}:{val}}}")
        rval = not val if is_complement(literal) else val
        return rval

    print(f"asgmt ({bvar} in {assignment}) => {{{bvar}:{assignment.get(bvar)}}}")
    base_val = assignment.get(bvar)
    if base_val != None:
        rval = not val if is_complement(literal) else val
        # return base_val if bvar == literal else not base_val
    return


# def literal_value(lit: str, assignment: dict) -> bool:
#     var = base_var(lit)
#     val = assignment.get(var)
#     print(f"result: base({lit})={var} ({var}={val})")

#     val = not assignment.get(var) if is_complement(lit) else assignment.get(var)
#     print(f"result: {lit} value: {val} ({var}={assignment.get(var)})")
#     return val


def eval_clause(clause_assignment: dict) -> bool:
    print(f"eval {clause_assignment}")
    if any(clause_assignment) or (None in clause_assignment.values()):
        return True
    return False


# def evaluate_clause(var:str, assignment:dict, clauses:dict[int,list[str]]):
#     print(f"variable: {var}")
#     print(f"assignment: {assignment}")
#     print(f"clauses: {clauses}") # clauses with var literals
#     for clause_id,clause_literals in clauses.items():
#         literal_values = [assignment[literal] for literal in clause_literals]
#         print(f"{clause_id} literal_values: {literal_values}")


def evaluate_clause(clause_assignment: list) -> bool:
    """evaluate clause in cnf form (ie. sum assigned clause variables)"""
    value_sum = sum(clause_assignment)
    print(f"  clause evaluation(): value_sum: {value_sum}")
    return value_sum > 0


def parse_input(input_str: str) -> dict[int, list[str]]:
    """parse input expression into variables"""
    expression = input_str.replace(" ", "")

    literal_pattern = r"(\w+'?)"  # r"(x_\d+'?)"
    clause_pattern = r"\([^()]+\)"

    clauses = re.findall(clause_pattern, expression)
    clauses = {
        i: re.findall(literal_pattern, clause) for i, clause in enumerate(clauses)
    }
    return clauses


cnf_test_expressions = [
    "(X+Y)",
    "(X+Y')",
    "(X+Y)(X'+Y)",
    "(X+Y)(X'+Y')",
    "(x_1' + x_2)(x_1' + x_3)",
    "(x_1' + x_2 + x_4') (x_2 + x_3' + x_4) (x_1 + x_2' + x_3) (x_1 + x_2 + x_3)",
    "(x_1' + x_2 + x_4' + x_5') (x_2 + x_3 + x_5' + x_6') (x_1 + x_2 + x_3 + x_5)",
]


def main():
    # input and parse expression data
    input_str = cnf_test_expressions[1]
    print(f"input: {input_str}")
    clause_dict = parse_input(input_str)

    var_set: set[str] = set()
    constraints = {}
    for clause_id, literals in clause_dict.items():
        print(f"clause {clause_id} variables: [{', '.join(literals)}]")
        for var in literals:
            base_var = var.replace("'", "")
            var_set.add(base_var)
            constraints[base_var] = [literals]
    variables = order(var_set)

    # set variable domains
    # base_domain = (0, 1)  # (True,False)
    base_domain = (True, False)  # (True,False)
    domains = {var: base_domain for var in var_set}

    # constraints based on clauses
    csp = CSP(variables, domains, constraints)
    solution = csp.solve(backtrack)
    print(f"\nsolution: {solution}")


def main_1():
    # input and parse expression data
    input_str = cnf_test_expressions[2]
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
