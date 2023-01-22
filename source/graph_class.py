import re
from random import shuffle


class Graph:
    def __init__(self, graph_path, saved_as_directed):
        """
        :param graph_path: The relative path to the graph file, e.g., graphs/CA-AstroPh.txt
        :param saved_as_directed = True if only (v,u) is included in the file, not its symmetric (u,v)
        """
        self.graph, self.graph_edges = self.read_edge_list(graph_path, saved_as_directed)

    def read_edge_list(self, path, saved_as_directed):
        graph = {}
        graph_edges = []
        with open(path, "r") as edges:
            for edge in edges:
                if edge.startswith('#'):  # comment line
                    continue

                edge = re.split('\s+', edge)
                v, u = (int(edge[i]) for i in range(2))  # v -> u
                graph_edges.append((v, u))
                try:
                    graph[v].append(u)
                except KeyError:
                    graph[v] = [u]    # u is v's first neighbor
                if u not in graph:
                    graph[u] = []

                if saved_as_directed:
                    # Graph is considered undirected => also include (u,v)
                    # since it is not present in the file
                    graph_edges.append((u, v))
                    graph[u].append(v)

        return graph, graph_edges

    def nodes(self):
        """ :return: The nodes of the graph as a list """
        return [*self.graph]

    def neighbors(self, v):
        """
        :param v: A node in the graph
        :return: The list of v's neighbors. If v has no neighbors return an empty list
        """
        return self.graph.get(v, [])

    def degree(self, v):
        try:
            return len(self.neighbors(v))
        except TypeError:
            return None

    def delete_isolated_node(self, v):
        if self.degree(v) == 0 :
            del self.graph[v]

    def set_neighbors(self, v, neighbors):
        self.graph[v] = neighbors

    def graphAsStream(self):
        shuffle(self.graph_edges)
        return self.graph_edges

    def toString(self):
        print(self.graph)

    def adj_matrix(self):
        keys = sorted(self.graph.keys())
        size = len(keys)
        adj = [[0] * size for i in range(size)]

        # for a row in graph.items() iterates over the key:value entries in dictionary
        #  for b in row iterates over the values.
        for a, b in [(keys.index(a), keys.index(b)) for a, row in self.graph.items() for b in row]:
            adj[a][b] = 2 if (a == b) else 1  # 2 when the vertex has an edge to itself

        return adj