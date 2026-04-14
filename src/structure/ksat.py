from src.common import *
from src.structure.parsers import *

# --------------------------------------------------- #
# def is_ksat(clauses: list[c_type], k: int) -> bool:
# return all(len(clause) == k for clause in clauses)
def is_ksat(clauses, k: int) -> bool:
    return all(len(clause) == k for clause in clauses)


# def is_2sat(clauses: list[c_type]) -> bool:
#     return is_ksat(clauses, 2)
def is_2sat(expression, variables, literals, clauses) -> bool:
    return is_ksat(clauses, 2)


# def is_2sat(expression, variables, literals, clauses) -> bool:
#     return all(1 <= len(clause) <= 2 for clause in clauses)


# def is_3sat(clauses: list[c_type]) -> bool:
# return is_ksat(clauses, 2)
def is_3sat(expression, variables, literals, clauses) -> bool:
    return is_ksat(clauses, 2)


def to_2sat(expression, variables, literals, clauses: list[c_type]) -> list[c_type]:
    """convert set of clauses with 1 or 2 literlas in consistent 2CNF structure"""
    rclauses = []
    for clause in clauses:
        if len(clause) > 2:  # clause has too many literals
            dprint(f"clause {clause} has too many literals; must have <= 2")
            return None
        if len(clause) < 2:  # clause has 1 literal
            dprint(f"clause {clause} has 1 literal")
            clause += clause  # duplicate the clause
            dprint(f"clause => {clause}")
        rclauses.append(clause)
    dprint(f"returning: {rclauses}")
    return expression, variables, literals, rclauses



def test_to_2sat(expr_str):
    """
    used as helper in testing script (since to_2sat needs intermediate values: clauses)
    parses expression string, passes clause to conversion function
    """
    result = to_2sat(*parse_cnf_expression(expr_str))
    if isinstance(result, tuple):
        return result[-1]  # last element in tuple returned from to_2sat
    return result