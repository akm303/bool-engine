"""
Davis Putnam algorithm

Algorithm: Davis-Putnam(F)
Input: A formula (set of clauses) F

    if F has a unit-clause contradiction
        //must be unsatisfiable
        return false;
    endif

    if F has single-phase variables
        //bc we can make those clauses true
            remove their clauses from F;
    endif

    // now eliminate a var and its resolvents
    pick a variable x from those remaining
    F' = empty-set
    for each (x+A_i) and (x+B_j) in F:
        if (A_i + B_j) is not tautological:
            add(A_i + B_j) to F'
        endif
    endfor
    remove all clauses containing x or x' from F
    F = F AND all clauses in F'
    return Davis-Putnam(F)
"""

from pprint import pformat
from typing import Tuple

from src.solver.cnf_ksat import parse_cnf_expression, setup_ksat
from src.solver.cnf_ksat import req_2sat
from src.solver.cnf_ksat import WILDCARD
from src.common import *


# def get_unit_clause_contradictions(clauses: list[c_type]) -> list[v_type]:
#     """return list of variables that have unit-clause contradictions
#     eg. if clauses = [ (x), (x'), (y), (z'), (z)]
#         then return: ['x','z']
#     """
#     # get all unit clauses
#     # in 2CNF, any clause where both terms are the same literal
#     # ie. (x + x) and (x' + x') are unit clauses
#     # but (x + x') is not a unit clause
#     unit_clauses = [clause[0] for clause in clauses if clause[0] == clause[1]]
#     print(f"all unit clauses: {unit_clauses}")

#     contradictory_clauses = [
#         base_variable(uclause_var)
#         for uclause_var in unit_clauses
#         if neg(uclause_var) in unit_clauses
#     ]
#     contradictory_clauses = list(set(contradictory_clauses))
#     print(f"all contradictory unit clauses: {unit_clauses}")

#     return contradictory_clauses


def get_unit_clauses(clauses: list[c_type]) -> list[v_type]:
    """return list of variables that have unit-clause contradictions
    eg. if clauses = [ (x), (x'), (y), (z'), (z)]
        then return: ['x','z']
    """
    # get all unit clauses
    # in 2CNF, any clause where both terms are the same literal
    # ie. (x + x) and (x' + x') are unit clauses
    # but (x + x') is not a unit clause
    return [clause[0] for clause in clauses if clause[0] == clause[1]]


def get_single_phase_variables(literals):
    print(f"literals: {literals}")
    single_phase = [literal for literal in literals if neg(literal) not in literals]
    print(f"single_phase: {single_phase}")
    return single_phase


def remaining_variables(clauses) -> list[v_type]:
    variables = set()
    for clause in clauses:
        for literal in clause:
            variables.add(base_variable(literal))
    return list(variables)


def select_clauses(clauses, var):
    """select clauses containing variable"""
    return [clause for clause in clauses if ((var in clause) or (neg(var) in clause))]

def other_literal(clause,var):
    lit1,lit2 = clause
    return lit1 if var == lit2 else lit2


def is_satisfiable(expression, variables, literals, clauses):
    assignment = a_type()
    result, assignment = dp_algorithm(assignment, literals, clauses)
    return result, assignment


def dp_algorithm(assignment: a_type, literals: list[l_type], clauses: list[c_type]):
    if len(clauses) <= 0:
        result = bool(assignment)
        return result, assignment

    # check if F has a unit-clause contradiction
    unit_clauses = get_unit_clauses(clauses)
    print(f"  unit clauses: {unit_clauses}")
    contradictory_unit_clauses = [
        base_variable(uclause_var)
        for uclause_var in unit_clauses
        if neg(uclause_var) in unit_clauses
    ]
    contradictory_unit_clauses = list(set(contradictory_unit_clauses))
    print(f"  contradictory: {contradictory_unit_clauses}")
    if contradictory_unit_clauses:
        print("  F has unit clause contradictions => must be unsatisfiable")
        return False, contradictory_unit_clauses

    # check if F has single-phase variables; we can make those clauses true
    single_phase_literals = get_single_phase_variables(literals)
    print(f"  single phase variables: {single_phase_literals}")

    remaining_clauses = clauses.copy()
    for sp_lit in single_phase_literals:
        sp_var = base_variable(sp_lit)
        assignment[sp_var] = 0 if is_complement(sp_lit) else 1
        remaining_clauses = [clause for clause in remaining_clauses if sp_var not in clause]

    print(f"  assignment: {assignment}")
    print(f"  remaining_clauses: {remaining_clauses}")

    # # eliminate a var and its resolvents
    # ---
    # pick a variable x from those remaining
    # F' = empty-set
    # for each (x+A_i) and (x+B_j) in F:
    #     if (A_i + B_j) is not tautological:
    #         add(A_i + B_j) to F'
    #     endif
    # endfor
    # remove all clauses containing x or x' from F
    # F = F AND all clauses in F'
    # return Davis-Putnam(F)

    rem_variables = remaining_variables(remaining_clauses)
    print(f"remaining_variables: {rem_variables}")

    if not rem_variables:
        return True, assignment

    var = rem_variables[0]

    # clauses containing x and x'
    pos_clauses = [c for c in remaining_clauses if var in c]
    neg_clauses = [c for c in remaining_clauses if neg(var) in c]

    Fprime = set()

    # resolution: (x + A_i) and (x' + B_j) -> (A_i + B_j)
    for c1 in pos_clauses:
        for c2 in neg_clauses:
            print(f"clause 1: {c1}")
            print(f"clause 2: {c2}")
            lit1 = other_literal(c1, var)
            lit2 = other_literal(c2, neg(var))

            # skip tautology
            if lit1 != neg(lit2):
                print(f" -> new clause: {(lit1, lit2)}")
                Fprime.add((lit1, lit2))
            else:
                assignment[base_variable(lit1)] = WILDCARD
                

            # # skip tautology
            # if lit1 == neg(lit2):
            #     continue

            # Fprime.add((lit1, lit2))

    # remove all clauses containing x or ¬x
    new_clauses = [
        c for c in remaining_clauses
        if var not in c and neg(var) not in c
    ]

    # add resolvents
    new_clauses.extend(list(Fprime))

    print(f"  F': {Fprime}")
    print(f"  new_clauses: {new_clauses}")

    return dp_algorithm(assignment, literals, new_clauses)

    # rem_variables = remaining_variables(remaining_clauses)
    # print(f"rem_variables: {rem_variables}")
    # if rem_variables:
    #     var = rem_variables.pop()
    #     Fprime = set()
    #     while len(select_clauses(remaining_clauses,var)) > 1:
    #         # remaining_clauses = [clause for clause in remaining_clauses if clause != clause1]
    #         clause1 = remaining_clauses.pop()
    #         clause2 = remaining_clauses.pop()
    #         print(f"  > clause1: {clause1}")
    #         print(f"  > clause2: {clause2}")

    #         lit1 = other_literal(clause1,var)
    #         lit2 = other_literal(clause2,var)
    #         print(f"  > lit1: {lit1}")
    #         print(f"  > lit2: {lit2}")
    #         if lit1 != neg(lit2):
    #             Fprime.add((lit1,lit2))
    #         # while len(select_clauses(remaining_clauses,var)) > 0:
    #         print(f"Fprime: {Fprime}")




# --------------------------------------------------- #
def run(cnf_expr: e_type, to_output="both", run_i: int = -1):
    print(bar40)
    print("2-SAT Solver (DP)")
    expression, variables, literals, clauses = setup_ksat(
        cnf_expr, restrictions=[req_2sat]
    )

    dprint()
    is_sat, evidence = is_satisfiable(expression, variables, literals, clauses)
    print()
    print(f"is satisfiable? {is_sat}")
    print(f"evidence: {evidence}")

    print(bar40)
    print()

    if to_output == "assignment":
        return evidence
    elif to_output == "is_sat":
        return is_sat
    else:
        return is_sat, evidence


def tests():
    # dictionary mapping an expression to whether or not its satisfiable
    cnf_test_expressions = {
        # custom examples
        "(X)": True,
        "(X')": True,
        "(X')(X')": True,
        "(X)(X)": True,
        "(X)(X')": False,
        "(X+Y)": True,
        "(X+Y')": True,
        "(X'+Y)": True,
        "(X'+Y')": True,
        "(X+Y)(X'+Y)": True,
        "(X+Y)(X'+Y')": True,
        "(x_1' + x_2)(x_1' + x_3)": True,
        # example from 2SAT on website
        "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1')": True,
        "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1') (x_3' + x_1)": False,
        "(x_2' + x_1) (x_1' + x_3) (x_3 + x_1) (x_3' + x_2') (x_3' + x_2)": False,  # swapped x_1 & x_2
        "(x_3' + x_2) (x_2' + x_1) (x_1 + x_2) (x_1' + x_3') (x_1' + x_3)": False,  # swapped x_1 & x_3
        # custom examples
        "(x_a' + x_a)": True,
        "(A + A)(A' + A')": False,
    }

    test_results = {}
    test_i = 0
    for cnf_expr, expected in cnf_test_expressions.items():
        test_i += 1
        is_sat = run(cnf_expr, "is_sat", test_i)
        test_passed = "Pass" if is_sat == expected else "Fail"
        print(f"test {test_i}: {test_passed}")

        test_results[test_i] = test_passed
        print(bar40)
        print()
    print()
    print(f"test results: {test_results}")
    print(
        "All Tests Passed"
        if all(result == "Pass" for result in test_results.values())
        else "Some Tests Failed"
    )


if __name__ == "__main__":
    dprint("running `dp_2sat.py`")
    dprint()
    args = parse_flags()
    set_debug(args.debug)
    if args.expression is not None:
        run(args.expression)
    else:
        tests()
else:
    dprint("importing `dp_2sat.py`")