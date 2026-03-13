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


cnf_test_expressions = [
    "(X+Y)",
    "(X+Y')",
    "(X'+Y)",
    "(X'+Y')",
    "(X+Y)(X'+Y)",
    "(X+Y)(X'+Y')",
    "(x_1' + x_2)(x_1' + x_3)",
    
    # example form 2SAT on website
    "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1')",  
    "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1') (x_3' + x_1)",  
]





# def connected_components(nodes:list[l_type],edges:list[Tuple[l_type,l_type]])->dict:
#     # def dfs(adjacents,visited)
#     pass

# def path_exists(l1:l_type,l2:l_type,edges:list[Tuple[l_type,l_type]]) -> bool:

def edges_from_clause(clause_2sat):
    u,v = clause_2sat
    edge1 = (neg(u),v)
    edge2 = (neg(v),u)
    return edge1,edge2



def get_edges_from_clauses(clauses):
    edges = []
    # implication graph: "if the literal u is true, then the literal v is true"
    # add 2 edges to implication graph for each pair of literals:
    # - (neg(u), v)
    # - (neg(v), u)
    for clause in clauses:
        edge1,edge2 = edges_from_clause(clause)
        edges.append(edge1)
        edges.append(edge2)

        dprint(bar40)
        dprint(f"clause: {c_str(clause)}")
        dprint(f" edge1: {edge_str(edge1)}")
        dprint(f" edge2: {edge_str(edge2)}")
        dprint(bar40)

        # connected_components[neg(u)].add(v)
        # connected_components[neg(v)].add(u)
    return edges

def main():
    cnf_expr = cnf_test_expressions[-2]
    expression, variables, literals, clauses = parse_cnf_expression(cnf_expr)

    # each clause has 2 literals because 2sat
    nodes = variables + [neg(var) for var in variables]
    edges = get_edges_from_clauses(clauses)
    
    print(f"nodes: {nodelist_str(nodes)}")
    print(f"edges: {edgelist_str(edges)}")

    adj_graph = build_adj_graph(nodes,edges)
    print(f"graph (adjacency): {adjgraph_str(adj_graph)}")
    
    dprint()
    dprint("reachable:")
    for node in adj_graph:
        reachables = get_reachable(node,adj_graph)
        dprint(f"from {node}: {nodelist_str(reachables)}")
    
    dprint()
    dprint("has_path(): from")
    for node1 in adj_graph:
        for node2 in adj_graph:
            dprint(f"  {node1} -> {node2} ? {has_path(node1,node2,adj_graph)}")
        dprint()



if __name__ == "__main__":
    args = parse_debug_flag()
    set_debug(args.debug)
    main()
