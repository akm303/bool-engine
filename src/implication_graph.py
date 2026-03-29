from typing import Tuple
from pprint import pformat

from common import *


# print = print_to_file(dprint, "stdout/implication_graph.tex")
# dprint = print_to_file(dprint, "debug/implication_graph.tex")


# -------------------------------- #
# Graph construction
def build_adj_graph(nodes: list[node_type], edges: list[edge_type]) -> graph_type:
    """build implication graph with vertices x_i and x_i' for each i"""
    adjacency = {n: set() for n in nodes}

    dprint("adding edges:")
    for edge in edges:
        dprint(
            f" {edge_str(edge)} to adj: {adjgraph_str(adjacency,one_line=True)}"
        )
        u, v = edge
        adjacency[u].add(v)
    return adjacency


def get_reachable(start_node: node_type, adj_graph: graph_type):

    def dfs(node: node_type, visited: set[node_type], adj_graph: graph_type):
        reachable = [node]
        visited.add(node)
        for adj_node in adj_graph[node]:
            if adj_node not in visited:
                reachable += dfs(adj_node, visited, adj_graph)
        return reachable

    reachable = dfs(start_node, set(), adj_graph)
    print(f"  reachable from {node_str(start_node)}: {nodes_str(reachable)}")
    return reachable[1:]


# ------------------------------ #
# ------------------------------ #

# does there exist a variable xi st. there is both
# - a path from xi to xi'
# - a path from xi' to xi


def has_path(u: node_type, v: node_type, graph: graph_type) -> bool:
    """returns whether node v can be reached from node u in graph g"""
    return (u == v) or (v in get_reachable(u, graph))


def main():
    pass


if __name__ == "__main__":
    main()
