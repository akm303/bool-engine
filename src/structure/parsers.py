from src.common import *

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

