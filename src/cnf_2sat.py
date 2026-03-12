"""
algorithm as based on [Extreme Algorithms](https://www2.seas.gwu.edu/~simhaweb/champalg/sat/sat.html) page: algorithm due to Apvall, Plass, and Tarjan

- for any CNF expression C, you can construct corresponding 3CNF expression C' st:
    C is satisfiable iff C' is satisfiable
- 2SAT is polynomially solvable
"""
from typing import Tuple
from pprint import pformat

from cnf_ksat import parse_cnf_expression
from implication_graph import build_adj_graph,adj_graph_str,get_reachable,edge_str
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
    # "(x_1' + x_2) (x_2' + x_3) (x_3 + x_2) (x_3' + x_1') (x_3' + x_1)",  
]





# def connected_components(nodes:list[l_type],edges:list[Tuple[l_type,l_type]])->dict:
#     # def dfs(adjacents,visited)
#     pass

# def path_exists(l1:l_type,l2:l_type,edges:list[Tuple[l_type,l_type]]) -> bool:

def implication_edges_from_clause(clause):
    u,v = clause
    edge1 = (neg(u),v)
    edge2 = (neg(v),u)
    return edge1,edge2



def get_edges_from_clauses(nodes, clauses):
    clauses_2sat = clauses
    edges = []
    
    # connected_components = {node:{node,} for node in nodes}
    connected_components = {node:set() for node in nodes}


    
    def propogate_connected_components(start_node,end_node,previous_nodes:set,connected_components:dict[l_type,set],level=0):
        dprint()
        dprint(f":: {level} from: {start_node} to {end_node}")
        # print(f"pre:\n{pformat(connected_components)}")
        dprint(f"cc_pre:{connected_components}")


        previous_nodes.add(start_node)
        connected_literals = connected_components[start_node]
        dprint(f"  > visited nodes: {previous_nodes}")
        dprint(f"  > connected to: {connected_literals}")

        for literal in connected_literals - previous_nodes:
            # print(f"  > prop {end_node} to {literal} (in {connected_components})")
            propogate_connected_components(literal,end_node,previous_nodes,connected_components,level+1)

        connected_literals.add(end_node)
        dprint(f"cc_pst:{connected_components}")
        # print(f"post:\n{pformat(connected_components)}")

    # implication graph: "if the literal u is true, then the literal v is true"
    # add 2 edges to implication graph for each pair of literals:
    # - (neg(u), v)
    # - (neg(v), u)
    for clause_2sat in clauses_2sat:
        dprint(bar40)
        edge1,edge2 = implication_edges_from_clause(clause_2sat)
        dprint(f"edge: {edge_str(edge1)}")
        dprint(f"from: {edge1[0]} -> {lset_str(connected_components[edge1[0]])} + {{{edge1[1]}}}")
        text = f"cc from: {connected_components}\n"
        edges.append(edge1)
        propogate_connected_components(edge1[0],edge1[1],set(),connected_components)
        text += f"cc   to: {connected_components}\n"
        dprint(text)
        dprint()
        

        dprint(f"edge: {edge_str(edge2)}")
        dprint(f"from: {edge2[0]} -> {lset_str(connected_components[edge2[0]])} + {{{edge2[1]}}}")
        text = f"cc from: {connected_components}\n"
        edges.append(edge2)
        propogate_connected_components(edge2[0],edge2[1],set(),connected_components)
        text += f"cc   to: {connected_components}\n"
        dprint(text)
        dprint()
        dprint(bar40)

        # connected_components[neg(u)].add(v)
        # connected_components[neg(v)].add(u)
    return edges

def main():
    cnf_expr = cnf_test_expressions[-1]
    expression, variables, literals, clauses = parse_cnf_expression(cnf_expr)

    # each clause has 2 literals because 2sat
    nodes = variables + [neg(var) for var in variables]
    edges = get_edges_from_clauses(nodes,clauses)
    
    print(f"nodes: {nodes}")
    print(f"edges: {edges}")

    adj_graph = build_adj_graph(nodes,edges)
    print(f"adj_graph_str: {adj_graph_str(adj_graph)}")
    
    print()
    print("reachable:")
    for node in adj_graph:
        reachables = get_reachable(node,adj_graph)
        print(f"from {node}: {reachables}")
    pass


if __name__ == "__main__":
    args = parse_debug_flag()
    set_debug(args.debug)
    main()
