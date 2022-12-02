import re


class Graph:
    def __init__(self, graph_path):
        self.graph = self.read_edge_list(graph_path)

    def read_edge_list(self, path):
        graph = {}
        with open(path, "r") as edges:
            for edge in edges:
                if edge.startswith('#'):  # comment line
                    continue

                edge = re.split('\s+', edge)
                v, u = (int(edge[i]) for i in range(2))  # v -> u
                try:
                    graph[v].append(u)
                except KeyError:
                    graph[v] = [u]    # u is v's first neighbor
                if u not in graph:
                    graph[u] = []
        return graph

    def nodes(self):
        return [*self.graph]

    def neighbors(self, v):
        return self.graph.get(v, None)

    def degree(self, v):
        try:
            return len(self.neighbors(v))
        except TypeError:
            return None

    def toString(self):
        print(self.graph)
