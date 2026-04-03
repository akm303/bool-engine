"""
algorithm as based on [Extreme Algorithms](https://www2.seas.gwu.edu/~simhaweb/champalg/sat/sat.html) page
based initially on algorithm by Apsvall, Plass, and Tarjan
(true-to-source implementation of Apsvall, Plass, Tarjan in `cnf_apt.py`)

- for any CNF expression C, you can construct corresponding 3CNF expression C' st:
    C is satisfiable iff C' is satisfiable
- 2SAT is polynomially solvable





From " A LINEAR-TIME ALGORITHM FOR TESTING THE TRUTH OF CERTAIN QUANTIFIED BOOLEAN FORMULAS"
By Apsvall, Plass, Tarjan

Graph G(F) is a directed graph constructed from quantified boolean formula with no free variables:
    - F = Q1x1 Q2x2 Q3x3 ... Qnxn C 
    st. C is in CNF with at most 2 literals per clause
one-literal clauses are equivalent to a two literal ORing of itself (ie. "(u)" = "(u + u)")

1. construct a digraph G(F) with 2n vertices and 2|C| edges st:
    .1 for each variable xi, we add vertices xi and xi'
    .2 for each clause (u + v), add edges (u'->v) and (v'->u)
    - duality property: G(F) is isomorphic to graph obtained from G(F) by:
        reversing the directions of all edges 
        and complementing the names of all vertices


Tarjan's Linear Time Algorithm:
finds strong components of a directed graph 
    (ie. finds if there is a path from any vertex to any other)
by generating components in reverse topological order
    (ie. in an order st. if (S1 is generated before S2) => (S1 is not a predecessor of S2))

suppose we assign Truth values to vertices of G(F)
assignment corresponds to a set of truth values for varuables which makes C true iff 
    - forall i, vertices xi and xi' receive complementary truth values
    - no edge u->v has u assigned true and v assigned false
        ie. no path leads froma true vertex to a false vertex

Consider the SAT problem; Thus, assume all quantifiers in F are existential:
    Thrm1: C is only satisfiable iff in G(F), vertex u_i is in the same strong component as its complement ui'
    (ie. no strong component S is equal to its complement S')

2SAT Algo:
- process strong components of S of G(F) in reverse topological order as follows:
    General Step: 
    if S is marked: do nothing
    else, if S=S': stop. C is unsatisfiable.
    else: mark S true and S' false


"""

from typing import Tuple
from pprint import pformat

from cnf_ksat import setup_ksat, is_2sat
from implication_graph import *
from common import *


# test outputs to tests directory
# print = print_to_file(print,"stdout/cnf_2sat.tex")
# dprint = print_to_file(dprint, "debug/cnf_2sat.tex")

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
    variables: list[v_type], adj_graph: graph_type, get_all_contradictions: bool = False
) -> Tuple[bool, list]:
    """
    returns whether or not an expression is satisfiable based on an implication graph
    """
    contradictions = []
    for n in variables:  # for each node n
        negn = neg(n)
        n_str, negn_str = sfmt(n, negn, fmt=node_str)
        found_n_to_negn_path = has_path(n, negn, adj_graph)
        found_negn_to_n_path = has_path(negn, n, adj_graph)
        dprint(f"checking for contradictory paths (@ {n_str})")
        # dprint(f"  from {n_str} -> {negn_str}")
        dprint(f"  has_path({n_str},{negn_str})? {found_n_to_negn_path}")
        dprint(f"  has_path({negn_str},{n_str})? {found_negn_to_n_path}")
        if found_n_to_negn_path and found_negn_to_n_path:
            print(f" ! found bidirectional paths between [ {n_str} <=> {negn_str} ]")
            contradictions.append((n, negn))
            if not get_all_contradictions:
                return False, contradictions
    return len(contradictions) <= 0, contradictions


def run(cnf_expr, run_i=-1):
    print(bar40)
    print("2-SAT Solver (custom)")
    expression, variables, literals, clauses = setup_ksat(cnf_expr,restrictions=[is_2sat])

    # each clause has 2 literals because 2sat
    nodes = nodes_from_variables(variables)
    edges = edges_from_clauses(clauses)
    adj_graph = build_adj_graph(nodes, edges)

    # expr_counter_str = f" {run_i+1}" if run_i > -1 else " "
    # test_title = f"expression{expr_counter_str} ::"

    # print(f'{test_title}   "{cnf_expr}"')
    # print(f'(formatted) ie.  "{expression}"')
    # # print(f'{" "*(len(test_title)-3)}ie.  "{expression}"')
    print()
    print(f"nodes: {nodelist_str(nodes)}")
    print(f"edges: {edgelist_str(edges)}")
    print(f"graph (adjacency): {adjgraph_str(adj_graph,indent='  ')}")

    # * do not remove, only comment
    # dprint()
    # paths = {}
    # for node1 in adj_graph:
    #     paths[node1] = {}
    #     for node2 in adj_graph:
    #         paths[node1][node2] = bool_num(has_path(node1, node2, adj_graph))
    #     dprint(f"  path exists from {node_str(node1)} to {a_str(paths[node1])}")

    print()
    is_sat, contradiction = is_satisfiable(
        variables, adj_graph, get_all_contradictions=True
    )
    print(f"is satisfiable? {is_sat}")
    if not is_sat:
        print(f"evidence: paths exist between {contradiction}")
    
    print(bar40)
    print()
    return is_sat


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
        is_sat = run(cnf_expr, test_i)
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
    args = parse_flags()
    set_debug(args.debug)
    if args.expression is not None:
        run(args.expression)
    else:
        tests()
