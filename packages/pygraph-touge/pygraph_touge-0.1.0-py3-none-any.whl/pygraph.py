from collections import defaultdict
from typing import Dict, Set, Tuple, Union, Iterable


Node = Union[str, int]
Edge = Tuple[Node, Node]


class Graph(object):
    """Graph data structure, undirected by default."""

    def __init__(self, edges: Iterable[Edge] = [], directed: bool = False):
        self._graph: Dict[Node, Set[Node]] = defaultdict(set)
        self._directed = directed
        for edge in edges:
            self.add_edge(edge)

    def has_node(self, node: Node):
        """Whether a node is in graph"""
        return node in self._graph

    def has_edge(self, edge: Edge):
        """Whether an edge is in graph"""
        return edge[0] in self._graph and edge[1] in self._graph[edge[0]]

    def add_node(self, node: Node):
        """Add a node"""
        if node not in self._graph:
            self._graph[node] = set()

    def add_edge(self, edge: Edge):
        """Add an edge (node1, node2). For directed graph, node1 -> node2"""
        self._graph[edge[0]].add(edge[1])
        if self._directed:
            if edge[1] not in self._graph:
                self._graph[edge[1]] = set()
        else:
            self._graph[edge[1]].add(edge[0])

    def remove_node(self, node: Node):
        """Remove all references to node"""
        if node not in self._graph:
            raise ValueError(f"{node} not in graph!")
        for _, edges in self._graph.items():
            if node in edges:
                edges.remove(node)
        del self._graph[node]

    def remove_edge(self, edge: Edge):
        """Remove an edge from graph"""
        node1, node2 = edge
        if node1 in self._graph:
            self._graph[node1].remove(node2)
            if not self._directed:
                self._graph[node2].remove(node1)
        else:
            raise ValueError(f"{edge} not in graph!")

    def indegree(self, node: Node) -> int:
        """Compute indegree for a node"""
        if node not in self._graph:
            raise ValueError(f"{node} not in graph")
        indegree = 0
        for _, connections in self._graph.items():
            if node in connections:
                indegree += 1
        return indegree

    def outdegree(self, node: Node) -> int:
        """Compute outdegree for a node"""
        if node not in self._graph:
            raise ValueError(f"{node} not in graph")
        return len(self._graph[node])

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, dict(self._graph))

    def __repr__(self):
        return str(self)
