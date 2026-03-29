"""
algorithm as based on [Extreme Algorithms](https://www2.seas.gwu.edu/~simhaweb/champalg/sat/sat.html) page
true-to-source implementation of algorithm defined by Apsvall, Plass, and Tarjan algorithm from their paper:
"A LINEAR-TIME ALGORITHM FOR TESTING THE TRUTH OF CERTAIN QUANTIFIED BOOLEAN FORMULAS"

Main Idea:
- assign truth values to nodes of $G(F)$ st
    - $\forall i$, nodes $x_i$ and $\bar{x_i}$
- find strongly connected subcomponents $S$ of graph $G(F)$ representing 2sat formula $F$

Graph G(F) is a directed graph constructed from quantified boolean formula with no free variables:
    - F = Q1x1 Q2x2 Q3x3 ... Qnxn C
    st. C is in CNF with at most 2 literals per clause
one-literal clauses are equivalent to a two literal ORing of itself (ie. "(u)" = "(u + u)")

1. construct a digraph G(F) with 2n vertices and 2|C| edges st:
    1.1 for each variable xi, we add vertices xi and xi'
    1.2 for each clause (u + v), add edges (u'->v) and (v'->u)
    - duality property: G(F) is isomorphic to graph obtained from G(F) by:
        reversing the directions of all edges
        and complementing the names of all vertices


2. Tarjan's Algorithm to find strong components of a directed graph in O(n)
by generating components in reverse topological order
    - finds if there is a path from any vertex to any other
    - in an order st. if (S1 is generated before S2) => (S1 is not a predecessor of S2)



def:
    If S1 and S2 are strong components such that
    an edge leads from vertex in S1 to a vertex in S2,
    then S1 is a predecessor of S2
    and S2 is a successor of S1.

an assignment corresponds to set of truth value that make $F$ true $\iff$:
    2.1 $\forall$ nodes, $x$ and $x'$ receive complementary truth values
    2.2 no edge $u -> v$ has u assigned true and v assigned false (ie. no path leads from a true node to false node)


3. 2CNF Evaluation algorithm to prove Theorem 2
Process strong components S of G(F) in reverse topological order as follows:
    (1)
    - if S is marked: go to next component
    - else if some successor of S is marked false or contingent: goto (2)
    - else: goto (3)

    (2) // S has a false or contingent successor
    - if S contains one or more universal vertices: stop (3.3 holds)
    - else: mark S false, goto 5

    (3) // all successors of S are true
    - if S contains 2+ universal vertices: stop; condition 2.3 holds
    - else if S contains one universal variable ui: goto (4)
    - else: mark S true and goto (5)

    (4) // S contains a universal vertex ui
    - if S contains an existential vertex uj with j < i: stop; condition 3.2 holds
    - else: mark S ***contingent*** and goto (5)

    (5) // S is marked successfully
    - if S=S': stop; condition 3.1 or 3.2 holds
    - else: goto (6)

    (6) // $S≠\bar{S}$
    - if $S$ is marked contingent or false and $\bar{S}$ is a predecessor of $S$: stop; condition 2.3 holds
    - else: mark $\bar{S}$ false if $S$ is true, contingent if $S$ is contingent, and true if $S$ is false




Theorem 2
formula F is true iff none of the following three conditions hold:
    3.1 an existential vertex u is in the same strong component as its complement u'
    3.2 a universal vertex ui is in the same strong component as an existential vertex uj st. j<i
        (ie. xj is not quantified within the scope of Qi)
    3.3 there is a path from a universal vertex u to another universal vertex v
        (this condition includes the case that v=u')




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

from typing import Tuple, Iterator
from pprint import pformat

from cnf_ksat import parse_cnf_expression, is_2sat
from implication_graph import build_adj_graph, has_path
from common import *


# test outputs to tests directory
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


# Tarjan's Algorithm to generate Strong Components of graph
def gen_strong_components(adj_graph: graph_type) -> Iterator[list[node_type]]:
    """
    Takes a directed graph as input
    produces a partition of the graph's vetices into the graph's strongly connected components (scc)
    each vertex appears in exactly one scc

    """

    def strongconnect(v: node_type, i: int, index: dict, lowlink: dict):
        # set depth index for v to smallest unused index
        index[v] = i[0]
        lowlink[v] = i[0]
        i[0] += 1
        stack.append(v)

        print()
        print(f"  index: {index}")
        print(f"  lowlink: {lowlink}")
        print(f"  stack: {stack}")

        # consider v's successors
        for w in adj_graph.get(v, []):
            print(f"  adj_graph[{v}] -> w={w}")

            # if not index.get(w, None):
            if w not in index:
                # not yet defined; recurse on it
                print(f"    ({w} not yet defined; recurse on {w})")
                yield from strongconnect(w, i, index, lowlink)
                print(
                    f"    (1) lowlink[{v}] <- min(lowlink[{v}]={lowlink[v]}, lowlink[{w}]={lowlink[w]})"
                )
                lowlink[v] = min(lowlink[v], lowlink[w])

            elif w in stack:
                # w is in stack S, hence in current SCC
                # otherwise (v,w) is an edge pointing to an SCC already found, must be ignored
                print(f"    ({w} already in stack)")
                print(
                    f"    (2) lowlink[{v}] <- min(lowlink[{v}]={lowlink[v]}, index[{w}]={index[w]})"
                )
                lowlink[v] = min(lowlink[v], index[w])

        # if v is root node, pop the stack and gen an scc
        print()
        print(f":: stack: {stack}")
        print(f":: index: {index}")
        print(f":: lowlink: {lowlink}")
        print(f":: v = {v}")

        if lowlink[v] == index[v]:  # if head-node of scc, pop stack and store
            component = set()  # start new strongly connected component
            w = stack.pop()
            component.add(w)

            print(f"  w={w} <- stack: {stack}")
            print(f"  adding {w} to scc={component}")

            while w != v:  # and len(stack) > 0 :
                w = stack.pop()
                component.add(w)
                print(f"  > adding {w} to scc={component}")
            print()
            print(f"  yielding scc={component}")
            yield component

    i = [0]
    index = {}
    lowlink = {}
    stack = list()

    for v in adj_graph:

        # if not index.get(v, None):
        if v not in index:
            # print()
            yield from strongconnect(v, i, index, lowlink)

    # edges = []
    # for u,neighbors in adj_graph.items():
    # edges += [(u,v) for v in neighbors]

    # def dfs(root: node_type, component: set, visited: set, graph: graph_type):
    #     unvisited = list(set(graph.keys()) - visited)
    #     print(f"U={unvisited}")

    #     if len(unvisited) <= 0:
    #         return

    #     neighbors = graph[root]
    #     for n in neighbors:
    #         visited.add(n)
    #         if n in unvisited:
    #             component.add(n)
    #     return


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
    expression, variables, literals, clauses = parse_cnf_expression(cnf_expr)
    assert is_2sat(clauses)

    expr_counter_str = f" {run_i+1}" if run_i > -1 else " "
    test_title = f"expression{expr_counter_str} ::"

    print(bar40)
    print("Apsvall, Plass, Tarjan  algorithm")
    print(f'{test_title}   "{cnf_expr}"')
    print(f'(formatted) ie.  "{expression}"')

    # 1. construct implication graph
    print("1. constructing implication graph")
    print()

    nodes = nodes_from_variables(variables)
    edges = edges_from_clauses(clauses)
    adj_graph = build_adj_graph(nodes, edges)
    print(f"nodes: {nodelist_str(nodes)}")
    print(f"edges: {edgelist_str(edges)}")
    print(f"graph (adjacency): {adjgraph_str(adj_graph,indent='  ')}")

    # 2. generate strong components
    print(pformat(adj_graph))
    test_graph = {
        'x_0': {'x_1'},
        'x_1': {'x_2'},
        'x_2': {'x_0'},  # cycle (SCC of size 3)
        'x_3': {'x_4'},
        'x_4': {'x_3'},  # cycle (SCC of size 2)
        'x_5': set(),  # singleton
    }


    component_gen = gen_strong_components(adj_graph)
    # component_gen = gen_strong_components(test_graph)
    print(component_gen)

    i = input()
    not_all_components = True
    all_components = []
    while i in ["\n", "", " "] and not_all_components:
        try:
            component = next(component_gen)
            all_components.append(component)
            print(f"<< component: {component} >>")
            i = input()
        except:
            not_all_components = False

    print(f"all strong components: {all_components}")

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
        # "(X+Y)": True,
        # "(X+Y')": True,
        # "(X'+Y)": True,
        # "(X'+Y')": True,
        # "(X+Y)(X'+Y)": True,
        # "(X+Y)(X'+Y')": True,
        # "(x_1' + x_2)(x_1' + x_3)": True,
        # example from 2SAT on website
        # "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1')": True,
        "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1') (x_3' + x_1)": False,
        # "(x_2' + x_1) (x_1' + x_3) (x_3 + x_1) (x_3' + x_2') (x_3' + x_2)": False,  # swapped x_1 & x_2
        # "(x_3' + x_2) (x_2' + x_1) (x_1 + x_2) (x_1' + x_3') (x_1' + x_3)": False,  # swapped x_1 & x_3
        # custom examples
        # "(x_a' + x_a)": True,
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
