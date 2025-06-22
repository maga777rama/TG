from typing import Dict, List, Tuple, Optional, Union
import copy
import os

class GraphError(Exception):
    pass

class Graph:
    def __init__(self, directed: bool = False, weighted: bool = False):
        self.adjacency_list: Dict[str, List[Tuple[str, Optional[float]]]] = {}
        self.directed = directed
        self.weighted = weighted

    @classmethod
    def from_file(cls, filepath: str) -> 'Graph':
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File '{filepath}' does not exist.")

        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        header = lines[0].strip().split()
        if len(header) != 2:
            raise GraphError("Invalid header in file. Expected: '<directed> <weighted>'")

        directed = header[0].lower() == 'true'
        weighted = header[1].lower() == 'true'

        graph = cls(directed=directed, weighted=weighted)

        for line in lines[1:]:
            parts = line.strip().split()
            if not parts:
                continue
            src = parts[0]
            graph.add_vertex(src)
            for edge in parts[1:]:
                if weighted:
                    if ':' not in edge:
                        raise GraphError(f"Expected weight in format 'vertex:weight', got '{edge}'")
                    dst, weight = edge.split(':')
                    graph.add_edge(src, dst, float(weight))
                else:
                    graph.add_edge(src, edge)
        return graph

    @classmethod
    def copy(cls, other: 'Graph') -> 'Graph':
        new_graph = cls(directed=other.directed, weighted=other.weighted)
        new_graph.adjacency_list = copy.deepcopy(other.adjacency_list)
        return new_graph

    def add_vertex(self, vertex: str):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, u: str, v: str, weight: Optional[float] = None):
        if self.weighted and weight is None:
            raise GraphError("Weighted graph requires weight for edge.")
        if not self.weighted:
            weight = None

        if u not in self.adjacency_list:
            self.add_vertex(u)
        if v not in self.adjacency_list:
            self.add_vertex(v)

        self.adjacency_list[u].append((v, weight))
        if not self.directed:
            self.adjacency_list[v].append((u, weight))

    def remove_vertex(self, vertex: str):
        if vertex not in self.adjacency_list:
            raise GraphError(f"Vertex '{vertex}' does not exist.")
        del self.adjacency_list[vertex]

        for u in self.adjacency_list:
            self.adjacency_list[u] = [pair for pair in self.adjacency_list[u] if pair[0] != vertex]

    def remove_edge(self, u: str, v: str):
        if u not in self.adjacency_list or v not in self.adjacency_list:
            raise GraphError("One or both vertices do not exist.")

        self.adjacency_list[u] = [pair for pair in self.adjacency_list[u] if pair[0] != v]
        if not self.directed:
            self.adjacency_list[v] = [pair for pair in self.adjacency_list[v] if pair[0] != u]

    def to_edge_list(self) -> List[Tuple[str, str, Optional[float]]]:
        edges = []
        visited = set()
        for u in self.adjacency_list:
            for v, w in self.adjacency_list[u]:
                if self.directed or (u, v) not in visited and (v, u) not in visited:
                    edges.append((u, v, w))
                    visited.add((u, v))
        return edges

    def export_to_file(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{self.directed} {self.weighted}\n")
            for u in self.adjacency_list:
                edges = self.adjacency_list[u]
                line = u
                for v, w in edges:
                    if self.weighted:
                        line += f" {v}:{w}"
                    else:
                        line += f" {v}"
                f.write(line + '\n')

    def __str__(self):
        result = [f"Graph(directed={self.directed}, weighted={self.weighted})"]
        for u in self.adjacency_list:
            neighbors = ", ".join(f"{v}:{w}" if w is not None else v for v, w in self.adjacency_list[u])
            result.append(f"{u} -> {neighbors}")
        return "\n".join(result)
