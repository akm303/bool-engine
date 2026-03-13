from typing import Tuple
from pprint import pformat

from cnf_ksat import parse_cnf_expression
from common import *


node_type = str
edge_type = Tuple[str,str]
graph_type = dict[node_type,set[node_type]]

# -------------------------------- #
# Graph string formatting
def node_str(node:node_type) -> str:
    return node if is_complement(node) else node + " "


def nodelist_str(edges:list[node_type]) -> str:
    return "[" + ", ".join([node_str(e) for e in edges]) + "]"


def edge_str(edge:edge_type) -> str:
    return f"({node_str(edge[0])}, {node_str(edge[1])})"


def edgelist_str(edges:list[edge_type]) -> str:
    return "[" + ", ".join([edge_str(e) for e in edges]) + "]"


def adjgraph_str(adj_graph: graph_type, indent_str:str=" ", term_spacer:str="\n") -> str:
    terms = []
    for literal, adj_literal_set in adj_graph.items():
        terms.append(f"{indent_str}{node_str(literal)}: {lset_str(adj_literal_set)}")
    outstring = f",{term_spacer}".join(terms)
    return f"{{{term_spacer}{outstring}{term_spacer}}}"


# -------------------------------- #
# Graph construction
def build_adj_graph(nodes: list[node_type], edges: list[edge_type]) -> graph_type:
    """build implication graph with vertices x_i and x_i' for each i"""
    adjacency = {n: set() for n in nodes}

    for edge in edges:
        dprint(f"adding edge: {edge_str(edge)} to adj: {adjgraph_str(adjacency,term_spacer=' ')}")
        u, v = edge
        adjacency[u].add(v)
    return adjacency



def get_reachable(start_node:node_type, adj_graph:graph_type):

    def dfs(node: node_type, visited: set[node_type], adj_graph: graph_type):
        reachable = [node]
        visited.add(node)
        for adj_node in adj_graph[node]:
            if adj_node not in visited:
                reachable += dfs(adj_node, visited, adj_graph)
        return reachable

    reachable = dfs(start_node, set(), adj_graph)
    return reachable[1:]



# ------------------------------ #
# ------------------------------ #

# does there exist a variable xi st. there is both
# - a path from xi to xi'
# - a path from xi' to xi

def has_path(u:node_type,v:node_type,g:graph_type)->bool:
    """returns whether node v can be reached from node u in graph g"""
    return (u==v) or (v in get_reachable(u,g))


def main():
    pass


if __name__ == "__main__":
    main()
