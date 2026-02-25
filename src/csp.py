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
        print(f"self.variables: {self.variables}")
        print(f"self.domains: {self.domains}")
        print(f"assignment (pre): {assignment}")
        self.solution = self.algorithm(
            self.variables, self.domains, self.constraints, assignment
        )
        print(f"assignment (post): {assignment}")
        return self.solution


# Backtrack & helper functions
def is_complete(variables: list, assignment: dict):
    print(f"is_complete: variables {variables}, assignment {assignment}")
    return len(assignment) == len(variables)


def select_unassigned_variable(variables: list, domains: dict, assignment: dict):
    print()
    unassigned_vars = [var for var in variables if var not in assignment]
    print(
        f"assignment: {assignment}, variables: {variables}, unassigned: {unassigned_vars}"
    )
    return min(unassigned_vars, key=lambda var: len(domains[var]))
    # unassigned_vars = [var for var in variables if var not in assignment]
    # return min(unassigned_vars, key=lambda var: len(domains[var]))


def order_domain_values(var: str, domains: dict, assignment: dict):
    return domains[var]


def is_consistent(var: str, value: int, constraints: dict, assignment: dict) -> bool:
    # @param {dict} constraints: {var:complement(var)}
    #       contains var's complement. if var and its complement assigned the same value, false
    # valid_complements: bool = (constraints[var] in assignment) and (
    #     assignment[constraints[var]] == assignment[var]
    # )
    valid_complements: bool = (constraints[var] in assignment) and (
        value == assignment[var]
    )
    print(f"valid complements? {valid_complements} (var={var},val={value},constraints={constraints},assignment={assignment})")
    return valid_complements  # and evaluates_to_true


def backtrack(variables: list, domains: dict, constraints: dict, assignment: dict):
    if is_complete(variables, assignment):
        return assignment

    var = select_unassigned_variable(variables, domains, assignment)
    for value in order_domain_values(var, domains, assignment):
        if is_consistent(var, value, constraints, assignment):
            assignment[var] = value
            result = backtrack(variables, domains, assignment)
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


def order(var_set: set):
    return sorted(list(var_set))  # eg. (v1,v1',v2,v2',...)


def parse_input(input_str: str):
    """parse input expression into variables"""
    expression = input_str.replace(" ", "")

    var_pattern = r"(\w+'?)"  # r"(x_\d+'?)"
    clause_pattern = r"\([^()]+\)"

    clauses = re.findall(clause_pattern, expression)
    clauses = {i: re.findall(var_pattern, clause) for i, clause in enumerate(clauses)}
    return clauses


def complement(var):
    var_is_complement = "'" in var
    return var[:-1] if var_is_complement else var + "'"


def add_complements(variables: set, complements: dict):
    for var1 in variables:
        # associate var with its complement
        var2 = complement(var1)
        print(f"{var1:4}s complement is {var2:4}", end=" ")
        if var2 in variables:
            print("(in variables)")
            complements[var1] = var2
        else:
            print("(not in variables)")


def main():
    # input and parse expression data
    input_str = cnf_test_expressions[2]
    clause_dict = parse_input(input_str)

    var_set = set()
    for clause_id, variables in clause_dict.items():
        print(f"clause {clause_id}: variables [{', '.join(variables)}]")
        for var in variables:
            var_set.add(var)

    ordered_vars = order(var_set)
    print(f"var_set: {var_set}")
    print(f"order(var_set): {ordered_vars}")

    complements = {}
    for var in var_set:
        var_complement = complement(var)
        complements[var] = var_complement if var_complement in var_set else None
    print(f"complements: {complements}")

    # constraints = {}
    # for v,vc in complements.items():
    #     constraints[v] = []
    #     if vc:
    #         constraints[v].append((vc,0))
    #         constraints[v].append((vc,1))

    # print(f"constraints: {constraints}")

    base_domain = (0, 1)  # (True,False)

    # init results
    domains = {var: base_domain for var in var_set}

    csp = CSP(ordered_vars, domains, complements, backtrack)
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
    print(f"var set  : {var_set}")
    print(f"domains:\n{pformat(domain_dict,indent=2)}")

    active_complements = {var: None for var in var_set}
    add_complements(var_set, active_complements)
    print(f"complement_dict: {active_complements}")


main()
