from typing import Tuple
from pprint import pformat

from cnf_ksat import parse_cnf_expression
from common import *


def node_str(node):
    return node if is_complement(node) else node + " "


def edge_str(edge):
    return f"({node_str(edge[0])}, {node_str(edge[1])})"


def adj_graph_str(adj_graph: dict[str, set[str]], indent_str=" ", spacer="\n"):
    terms = []
    for literal, adj_literal_set in adj_graph.items():
        terms.append(f"{indent_str}{node_str(literal)}: {lset_str(adj_literal_set)}")
    outstring = f",{spacer}".join(terms)
    return f"{{{spacer}{outstring}{spacer}}}"


def build_adj_graph(nodes: list[str], edges: list[Tuple[str, str]]) -> dict:
    """build implication graph with vertices x_i and x_i' for each i"""
    adjacency = {n: set() for n in nodes}

    for edge in edges:
        dprint(f"adding edge: {edge_str(edge)} to adjacency: {adjacency}")
        u, v = edge
        adjacency[u].add(v)
    return adjacency


# def get_reachable(start_node, adj_graph):
#     def dfs(node:str,visited:set,adj_graph:dict) -> set:
#         visited.add(node)
#         reachable = {node,}
#         for adj_node in adj_graph[node]:
#             if adj_node not in visited:
#                 reachable = reachable.update(dfs(adj_node,visited,adj_graph))
#         return reachable
    
#     reachable = dfs(start_node,set(),adj_graph)
#     return reachable

def get_reachable(start_node, adj_graph):
    def dfs(node:str,visited:set,adj_graph:dict):
        visited.add(node)
        reachable = [node]
        for adj_node in adj_graph[node]:
            if adj_node not in visited:
                reachable += dfs(adj_node,visited,adj_graph)
        return reachable
    
    reachable = dfs(start_node,set(),adj_graph)
    return reachable


# print(bar40)
# print(pformat(edges))
# adj = {lit:set() for lit in nodes}
# adj = get_adjacency(edges,adj)
# print(f"adj: {adj}")


# def get_reachable(u,reachable:dict,visited:set=set()) -> dict:
#     """dfs to get all connected nodes to a node"""
#     visited.add(u)
#     print(f"visited: {visited} @ u={u}")
#     for v in reachable[u] - visited:
#         reachable = get_reachable(v,reachable,visited)

#     return reachable

# print(bar40)
# reach = adj.copy()
# print(f"reach: {reach}")
# reach = {lit:get_reachable(lit,reach,set()) for lit in nodes}


# ------------------------------ #
# ------------------------------ #

# does there exist a variable xi st. there is both
# - a path from xi to xi'
# - a path from xi' to xi


def main():
    pass


if __name__ == "__main__":
    main()
