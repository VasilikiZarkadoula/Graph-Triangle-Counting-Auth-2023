import re
from random import shuffle


class Graph:
    def __init__(self, graph_path, saved_as_directed, triest=False):
        """
        :param graph_path: The relative path to the graph file, e.g., graphs/CA-AstroPh.txt
        :param saved_as_directed = True if only (v,u) is included in the file, not its symmetric (u,v)
        """
        if not triest:
            # graph is represented as a dict of lists {node : list of neighbors}
            self.graph = self.read_edges_as_dictionary(graph_path, saved_as_directed)
        else:
            # graph is represented as a list of edges (list of tuples [(v,u)])
            self.graph = self.graphAsStream(graph_path, saved_as_directed)


    def read_edges_as_dictionary(self, path, saved_as_directed):
        graph = {}
        with open(path, "r") as edges:
            for edge in edges:
                if not edge[0].isdigit():  # comment line
                    continue

                edge = re.split('\s+', edge)
                v, u = (int(edge[i]) for i in range(2))  # v -> u
                try:
                    graph[v].append(u)
                except KeyError:
                    graph[v] = [u]    # u is v's first neighbor
                if u not in graph:
                    graph[u] = []

                if saved_as_directed:
                    # Graph is considered undirected => also include (u,v)
                    # since it is not present in the file
                    graph[u].append(v)

        return graph

    def graphAsStream(self, path, saved_as_directed):
        # Triest
        graph_edges = []
        with open(path, "r") as edges:
            for edge in edges:
                if not edge[0].isdigit():  # comment line
                    continue

                edge = re.split('\s+', edge)
                v, u = (int(edge[i]) for i in range(2))  # v -> u

                if saved_as_directed:
                    x = min(v, u)
                    y = max(u, v)
                    graph_edges.append((x, y))
                elif v < u:
                    graph_edges.append((v, u))

        shuffle(graph_edges)
        return graph_edges



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