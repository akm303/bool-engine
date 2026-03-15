from typing import Tuple
from pprint import pformat

from cnf_ksat import parse_cnf_expression
from common import *


node_type = str
edge_type = Tuple[str, str]
graph_type = dict[node_type, set[node_type]]


# -------------------------------- #
# Graph string formatting
def node_str(node: node_type) -> str:
    return node if is_complement(node) else node + " "


def edge_str(edge: edge_type) -> str:
    return f"( {node_str(edge[0])}, {node_str(edge[1])})"


def collection_str(objs: list[node_type], obj_fmt, braces: str, delim: str) -> str:
    return braces[0] + delim.join([obj_fmt(obj) for obj in objs]) + braces[1]


def nodes_str(nodes: list[node_type], braces="[]", delim=", ") -> str:
    return collection_str(nodes, node_str, braces=braces, delim=delim)


def edges_str(nodes: list[edge_type], braces="[]", delim=", ") -> str:
    return collection_str(nodes, edge_str, braces=braces, delim=delim)


def nodelist_str(nodes: list[node_type]) -> str:
    return nodes_str(nodes, braces="[]")


def edgelist_str(edges: list[edge_type]) -> str:
    return edges_str(edges, braces="[]")


def nodeset_str(nodes: set[node_type]) -> str:
    return nodes_str(nodes, braces=r"{}")


def edgeset_str(edges: list[edge_type]) -> str:
    return edges_str(edges, braces=r"{}")


def adjgraph_str(
    adj_graph: graph_type, indent: str = " ", one_line: bool = False
) -> str:
    spacer: str = "\n" if not one_line else " "
    terms = []
    for node, adj_nodes in adj_graph.items():
        terms.append(f"{indent}{node_str(node)}: {nodeset_str(adj_nodes)}")
    outstring = f",{spacer}".join(terms)
    return f"{{{spacer}{outstring}{spacer}}}"


# -------------------------------- #
# Graph construction
def build_adj_graph(nodes: list[node_type], edges: list[edge_type]) -> graph_type:
    """build implication graph with vertices x_i and x_i' for each i"""
    adjacency = {n: set() for n in nodes}

    for edge in edges:
        dprint(
            f"adding edge: {edge_str(edge)} to adj: {adjgraph_str(adjacency,one_line=True)}"
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
    # print(f"  reachable from {start_node}: {reachable}")
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
