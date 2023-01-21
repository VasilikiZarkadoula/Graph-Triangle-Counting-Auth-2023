from itertools import combinations


class NodeIterator:

    def __init__(self, graph, graph_edges):
        self.graph = graph
        self.graph_edges = set(graph_edges)

    def node_iterator(self):
        count_triangles = 0
        for node in self.graph.nodes():
            nbrs = []
            # find all pairs of neighbors {u,w} of node
            for u in self.graph.neighbors(node):
                nbrs.append(u)
            # create neighbor pairs of 2
            nbrs_pair = list(combinations(nbrs, 2))
            for u, v in nbrs_pair:
                # check if the pair is also an edge in the graph
                if (u, v) in self.graph_edges or (v, u) in self.graph_edges:
                    # to avoid double counting, we count a triangle only if u < n < w
                    if u < node < v:
                        count_triangles += 1
        return count_triangles
