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
    def __init__(self, variables: list, domains: list, constraints: list):
        self.variables: list = variables
        self.domains: list = domains
        self.constraints: list = constraints
        # self.algorithm = algorithm
        self.solution = None

    def solve(self):
        assignment = {}
        self.solution = self.backtrack(assignment)
        return self.solution

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [var for var in self.variables if var not in assignment]
        return min(unassigned_vars, key=lambda var: len(self.domains[var]))

    def order_domain_values(self, var, assignment):
        return self.domains[var]

    def is_consistent(self, var, value, assignment):
        for constraint_var in self.constraints[var]:
            if constraint_var in assignment and assignment[constraint_var] == value:
                return False
        return True


# Backtrack helper functions
def select_unassigned_variable(self, assignment):
    unassigned_vars = [var for var in self.variables if var not in assignment]
    return min(unassigned_vars, key=lambda var: len(self.domains[var]))


def order_domain_values(self, var, assignment):
    return self.domains[var]


def is_consistent(self, var, value, assignment):
    for constraint_var in self.constraints[var]:
        if constraint_var in assignment and assignment[constraint_var] == value:
            return False
    return True


# --------------------------------------------------- #


cnf_test_expressions = [
    "(x_1' + x_2)(x_1' + x_3)",
    "(x_1' + x_2 + x_4') (x_2 + x_3' + x_4) (x_1 + x_2' + x_3) (x_1 + x_2 + x_3)",
    "(x_1' + x_2 + x_4' + x_5') (x_2 + x_3 + x_5' + x_6') (x_1 + x_2 + x_3 + x_5)",
]


def output_result(result):
    """output solution to result.json"""
    with open("results.json", "w") as json_fp:
        json.dump(result, json_fp, indent=4)



def parse_input(input_str: str):
    """parse input expression into variables"""
    variable_pattern = r"(\w+'?)"  # r"(x_\d+'?)"
    clause_pattern = r"\([^()]+\)"

    expression = input_str.replace(" ", "")
    variables = re.findall(variable_pattern, expression)
    clauses = re.findall(clause_pattern, expression)

    out_str = (
        f'\nexpression     ({type(expression)}) :  "{expression}"'
        f"\nvariable_match ({type(variables)}): {variables}"
        f"\nclause_match   ({type(clauses)}): {clauses}"
    )
    print(out_str)
    return {
        "expression": input_str,
        "clauses": clauses,
        "variables": variables,
    }


def get_complement(var):
    var_is_complement = "'" in var
    return var[:-1] if var_is_complement else var+"'"

def add_complements(variables:set, complements:dict):
    for var1 in variables:
        # associate var with its complement
        var2 = get_complement(var1)
        print(f"{var1:4}s complement is {var2:4}",end=" ")
        if var2 in variables:
            print("(in variables)")
            complements[var1] = var2
        else:
            print("(not in variables)")


# def add_constraints(variables, constraints: dict):
#     for var1 in variables:
#         # associate var with its complement
#         var2 = get_complement(var1)
#         if var2 in variables:
#             constraints[var1].append(var2)
#             print(f"added {var2} to {var1} constraints")

    # constraints[var] = []
    # for i in range(9):
    #     if i != var[0]:
    #         constraints[var].append((i, var[1]))
    #     if i != var[1]:
    #         constraints[var].append((var[0], i))
    # sub_i, sub_j = var[0] // 3, var[1] // 3
    # for i in range(sub_i * 3, (sub_i + 1) * 3):
    #     for j in range(sub_j * 3, (sub_j + 1) * 3):
    #         if (i, j) != var:
    #             constraints[var].append((i, j))


# for expr in cnf_test_expressions:
#     parse_input(expr)


def main():
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

    active_complements = {var:None for var in var_set}
    add_complements(var_set,active_complements)
    print(f"complement_dict: {active_complements}")


main()
