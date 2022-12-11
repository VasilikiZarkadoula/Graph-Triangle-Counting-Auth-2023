from itertools import combinations


class NodeIterator:

    def __init__(self, graph, graph_edges):
        self.graph = graph
        self.graph_edges = graph_edges

    def sort_graph(self):
        self.graph = {key: sorted(self.graph[key]) for key in sorted(self.graph)}

    def node_iterator(self):

        self.sort_graph()
        nodes = self.graph.nodes()

        count_triangles = 0
        for node in nodes:
            nbrs = []
            # find all pairs of neighbors {u,w} of node
            for u in self.graph.neighbors(node):
                nbrs.append(u)
            # create neighbor pairs of 2
            nbrs_pair = list(combinations(nbrs, 2))
            for i in range(0, len(nbrs_pair)):
                if nbrs_pair[i] in self.graph_edges:
                    nbrs_pair[i] = tuple(nbrs_pair[i])
                    # to avoid double counting, we count a triangle only if u < n < w
                    if nbrs_pair[i][0] < node < nbrs_pair[i][1]:
                        count_triangles = count_triangles + 1
        return count_triangles
