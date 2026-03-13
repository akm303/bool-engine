"""
algorithm as based on [Extreme Algorithms](https://www2.seas.gwu.edu/~simhaweb/champalg/sat/sat.html) page: algorithm due to Apvall, Plass, and Tarjan

- for any CNF expression C, you can construct corresponding 3CNF expression C' st:
    C is satisfiable iff C' is satisfiable
- 2SAT is polynomially solvable
"""

from typing import Tuple
from pprint import pformat

from cnf_ksat import parse_cnf_expression
from implication_graph import *
from common import *


# cnf_test_expressions = [
#     "(X+Y)",
#     "(X+Y')",
#     "(X'+Y)",
#     "(X'+Y')",
#     "(X+Y)(X'+Y)",
#     "(X+Y)(X'+Y')",
#     "(x_1' + x_2)(x_1' + x_3)",
#     # example form 2SAT on website
#     "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1')",
#     "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1') (x_3' + x_1)",
# ]


cnf_test_expressions = {
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
}


def nodes_from_variables(variables):
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
        dprint(f"clause: {c_str(clause)}")
        dprint(f" edge1: {edge_str(edge1)}")
        dprint(f" edge2: {edge_str(edge2)}")
        dprint(bar40)

    return edges


def is_satisfiable(adj_graph: graph_type) -> Tuple[bool, list]:
    for n in adj_graph:  # for each node n
        if has_path(n, neg(n), adj_graph) and has_path(neg(n), n, adj_graph):
            return False, [n, neg(n)]
    return True, []


def tests():
    test_results = []
    for cnf_expr, expected in cnf_test_expressions.items():
        expression, variables, literals, clauses = parse_cnf_expression(cnf_expr)

        # each clause has 2 literals because 2sat
        nodes = nodes_from_variables(variables)
        edges = edges_from_clauses(clauses)

        print(bar40)
        print(f'expression: "{cnf_expr}"')
        print()
        print(f"nodes: {nodelist_str(nodes)}")
        print(f"edges: {edgelist_str(edges)}")

        adj_graph = build_adj_graph(nodes, edges)
        print(f"graph (adjacency): {adjgraph_str(adj_graph)}")

        dprint()
        dprint("reachable:")
        for node in adj_graph:
            reachables = get_reachable(node, adj_graph)
            dprint(f"from {node}: {nodelist_str(reachables)}")

        dprint()
        dprint("has_path(): from")
        for node1 in adj_graph:
            for node2 in adj_graph:
                dprint(f"  {node1} -> {node2} ? {has_path(node1,node2,adj_graph)}")
            dprint()

        is_sat, contradiction = is_satisfiable(adj_graph)
        print(f"is satisfiable? {is_sat}")
        if not is_sat:
            print(f"contradiction: {contradiction}")

        test_passed = "Pass" if is_sat == expected else "Fail"
        print(f"test: {test_passed}")

        # test_passed = is_sat == expected
        # print(f"test: {'Pass' if test_passed else 'Fail'}")

        test_results.append(test_passed)
        print(bar40)
        print()
    print()
    print(f"test results: {test_results}")


if __name__ == "__main__":
    args = parse_debug_flag()
    set_debug(args.debug)
    tests()
