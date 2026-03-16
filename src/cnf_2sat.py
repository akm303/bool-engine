"""
algorithm as based on [Extreme Algorithms](https://www2.seas.gwu.edu/~simhaweb/champalg/sat/sat.html) page: algorithm due to Apvall, Plass, and Tarjan

- for any CNF expression C, you can construct corresponding 3CNF expression C' st:
    C is satisfiable iff C' is satisfiable
- 2SAT is polynomially solvable
"""

from typing import Tuple
from pprint import pformat

from cnf_ksat import parse_cnf_expression, is_2sat
from implication_graph import *
from common import *


# --------------------------------------------------- #
# func alias
a_str = assignment_str


# --------------------------------------------------- #
# parsing functions - create nodes/edges from expression
def nodes_from_variables(variables):
    """return list of 'nodes' representing all implicated literals"""
    return variables + [neg(var) for var in variables]


def edges_from_clauses(clauses_2sat):
    """
    implication graph: "if the literal u is true, then the literal v is true"
    add 2 edges to implication graph for each pair of literals:
    - (neg(u), v)
    - (neg(v), u)
    """
    edges = []
    for clause in clauses_2sat:
        u, v = clause
        edge1 = (neg(u), v)
        edge2 = (neg(v), u)
        edges.append(edge1)
        edges.append(edge2)

        dprint(bar40)
        dprint(f"clause: {clause_str(clause)}")
        dprint(f" edge1: {edge_str(edge1)}")
        dprint(f" edge2: {edge_str(edge2)}")
        dprint(bar40)

    return edges


# --------------------------------------------------- #
# SAT check
def is_satisfiable(
    adj_graph: graph_type, get_all_contradictions: bool = False
) -> Tuple[bool, list]:
    """returns whether or not an expression is satisfiable based on an implication graph"""
    contradictions = []
    for n in adj_graph:  # for each node n
        negn = neg(n)
        n_str, negn_str = sfmt(n, negn, fmt=node_str)
        found_n_to_negn_path = has_path(n, negn, adj_graph)
        found_negn_to_n_path = has_path(negn, n, adj_graph)
        dprint(f"checking for contradictory paths")
        dprint(f"  from {n_str} -> {negn_str}")
        dprint(f"  has_path({n_str},{negn_str})? {found_n_to_negn_path}")
        dprint(f"  has_path({negn_str},{n_str})? {found_negn_to_n_path}")
        if found_n_to_negn_path and found_negn_to_n_path:
            print(f"  found bidir paths between [ {n_str} <=> {negn_str} ]")
            contradictions.append((n, negn))
            if not get_all_contradictions:
                return False, contradictions
    return len(contradictions) <= 0, contradictions


def tests():
    # dictionary mapping an expression to whether or not its satisfiable
    cnf_test_expressions = {
        # custom examples
        "(X+Y)": True,
        "(X+Y')": True,
        "(X'+Y)": True,
        "(X'+Y')": True,
        "(X+Y)(X'+Y)": True,
        "(X+Y)(X'+Y')": True,
        "(x_1' + x_2)(x_1' + x_3)": True,
        # example form 2SAT on website
        "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1')": True,
        "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1') (x_3' + x_1)": False,
        "(x_2' + x_1) (x_1' + x_3) (x_3 + x_1) (x_3' + x_2') (x_3' + x_2)": False,  # swapped x_1 & x_2
        "(x_3' + x_2) (x_2' + x_1) (x_1 + x_2) (x_1' + x_3') (x_1' + x_3)": False,  # swapped x_1 & x_3
        # custom examples
        "(x_a' + x_a)": True,
        "(A + A)(A' + A')": False,
    }

    test_results = {}
    i = 0
    for cnf_expr, expected in cnf_test_expressions.items():
        i += 1
        expression, variables, literals, clauses = parse_cnf_expression(cnf_expr)
        assert is_2sat(clauses)

        # each clause has 2 literals because 2sat
        nodes = nodes_from_variables(variables)
        edges = edges_from_clauses(clauses)
        adj_graph = build_adj_graph(nodes, edges)

        print(bar40)
        test_title = f"test {i} expression ::"
        print(f'{test_title}  "{cnf_expr}"')
        print(f'{" "*(len(test_title)-3)}ie.  "{expression}"')
        print()
        print(f"nodes: {nodelist_str(nodes)}")
        print(f"edges: {edgelist_str(edges)}")
        print(f"graph (adjacency): {adjgraph_str(adj_graph,indent='  ')}")

        dprint()
        dprint("reachable:")
        for node in adj_graph:
            reachables = get_reachable(node, adj_graph)
            dprint(f"from {node}: {nodelist_str(reachables)}")

        dprint()
        paths = {}
        for node1 in adj_graph:
            paths[node1] = {}
            for node2 in adj_graph:
                paths[node1][node2] = bool_num(has_path(node1, node2, adj_graph))
            dprint(f"  path exists from {node_str(node1)} to {a_str(paths[node1])}")

        dprint()
        is_sat, contradiction = is_satisfiable(adj_graph, get_all_contradictions=True)
        print(f"is satisfiable? {is_sat}")
        if not is_sat:
            print(f"evidence: paths exist between {contradiction}")

        test_passed = "Pass" if is_sat == expected else "Fail"
        print(f"test {i}: {test_passed}")

        # test_passed = is_sat == expected
        # print(f"test: {'Pass' if test_passed else 'Fail'}")

        test_results[i] = test_passed
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
    args = parse_debug_flag()
    set_debug(args.debug)
    tests()
