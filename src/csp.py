import json
import pprint
import argparse
import itertools
import re

from pprint import pformat

# from csp_objects import *
# from csp_solver import *


# CSP Problem definition
class CSP:
    def __init__(self, variables: list, domains: list, constraints: list, algorithm):
        self.variables: list = variables
        self.domains: list = domains
        self.constraints: list = constraints
        self.algorithm = algorithm
        self.solution = None

    def solve(self):
        assignment = {}
        print(f"variables: {self.variables}")
        print(f"domains: {self.domains}")
        print(f"constraints: {self.constraints}")
        print()
        self.solution = self.algorithm(
            self.variables, self.domains, self.constraints, assignment
        )
        print(f"\nresulting assignment: {assignment}")
        return self.solution


# Backtrack & helper functions
def is_complete(variables: list, assignment: dict):
    print(f"is_complete: variables {variables}, assignment {assignment}")
    return len(assignment) == len(variables)


def select_unassigned_variable(variables: list, domains: dict, assignment: dict):
    print()
    unassigned_vars = [var for var in variables if var not in assignment]
    # print(f"assignment: {assignment}, variables: {variables}, unassigned: {unassigned_vars}")
    return min(unassigned_vars, key=lambda var: len(domains[var]))
    # unassigned_vars = [var for var in variables if var not in assignment]
    # return min(unassigned_vars, key=lambda var: len(domains[var]))


def order_domain_values(var: str, domains: dict, assignment: dict):
    return domains[var]


def is_consistent(var: str, value: int, constraints: dict, assignment: dict) -> bool:
    # @param {dict} constraints: {var:complement(var)}
    #       contains var's complement. if var and its complement assigned the same value, false
    variable_clauses = constraints[var]
    print(f"is_consistent() => constraints[{var}]={variable_clauses}")

    clause_assignment = {}
    for constraint_set in variable_clauses:
        print(f"constraint_set: {constraint_set}")
        assignment_vals = [literal_value(lit,assignment) for lit in constraint_set]
        print(f"assignment_vals: {assignment_vals}")


    # clause_assignment = {
    #     literal: value if literal == var else literal_value(literal, assignment)
    #     for literal in constraints
    # }
    print(f"clause assignment: {clause_assignment}")
    if any(val == None for val in clause_assignment.values()):
        print("values unassigned, continuing")
        return True
    print(" (evaluating)")
    evaluate_clause(clause_assignment)
    return True
    # evaluate_clause(var,value,assigment)


def backtrack(variables: list, domains: dict, constraints: dict, assignment: dict):
    if is_complete(variables, assignment):
        return assignment

    var = select_unassigned_variable(variables, domains, assignment)
    for value in order_domain_values(var, domains, assignment):
        if is_consistent(var, value, constraints, assignment):
            assignment[var] = value
            result = backtrack(variables, domains, constraints, assignment)
            if result is not None:
                return result
            del assignment[var]
    return None


# --------------------------------------------------- #


def output_result(result):
    """output solution to result.json"""
    with open("results.json", "w") as json_fp:
        json.dump(result, json_fp, indent=4)


cnf_test_expressions = [
    "(x_1' + x_2)(x_1' + x_3)",
    "(x_1' + x_2 + x_4') (x_2 + x_3' + x_4) (x_1 + x_2' + x_3) (x_1 + x_2 + x_3)",
    "(x_1' + x_2 + x_4' + x_5') (x_2 + x_3 + x_5' + x_6') (x_1 + x_2 + x_3 + x_5)",
]


def order(var_set: set[str]) -> list[str]:
    return sorted(list(var_set))  # eg. (v1,v2,...)


def is_complement(var: str) -> bool:
    result = "'" in var
    print(f"  is_complement({var})? {result}")
    return result


def complement(lit: str) -> str:
    return lit[:-1] if is_complement(lit) else lit + "'"

def base_var(lit:str) -> str:
    result = lit if not is_complement(lit) else lit[:-1]
    return result

def literal_value(lit: str, assignment: dict) -> bool:
    var = base_var(lit)
    val = not assignment.get(var) if is_complement(lit) else assignment.get(var)
    # val = not assignment[var] if is_complement(lit) else assignment[var]
    print(f"result: {lit} value: {val} ({var}={assignment.get(var)})")
    return val


# def evaluate_clause(var:str, assignment:dict, clauses:dict[int,list[str]]):
#     print(f"variable: {var}")
#     print(f"assignment: {assignment}")
#     print(f"clauses: {clauses}") # clauses with var literals
#     for clause_id,clause_literals in clauses.items():
#         literal_values = [assignment[literal] for literal in clause_literals]
#         print(f"{clause_id} literal_values: {literal_values}")


def evaluate_clause(assignment: dict) -> bool:
    """evaluate clause in cnf form (ie. sum assigned clause variables)"""
    value_sum = sum(assignment.values())
    print(f"  clause evaluation(): value_sum: {value_sum}")
    return value_sum > 0


def parse_input(input_str: str) -> dict[int, list[str]]:
    """parse input expression into variables"""
    expression = input_str.replace(" ", "")

    var_pattern = r"(\w+'?)"  # r"(x_\d+'?)"
    clause_pattern = r"\([^()]+\)"

    clauses = re.findall(clause_pattern, expression)
    clauses = {i: re.findall(var_pattern, clause) for i, clause in enumerate(clauses)}
    return clauses


def main():
    # input and parse expression data
    input_str = cnf_test_expressions[2]
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
    base_domain = (0, 1)  # (True,False)
    domains = {var: base_domain for var in var_set}

    # constraints based on clauses

    csp = CSP(variables, domains, constraints, backtrack)
    # csp = CSP(ordered_vars,domains,constraints)
    solution = csp.solve()
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
