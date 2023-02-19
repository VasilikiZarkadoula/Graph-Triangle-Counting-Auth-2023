from itertools import combinations
from tqdm import tqdm


class NodeIterator:

    def __init__(self, graph):
        """
        :param graph: αντικείμενο της Graph
        """
        self.graph = graph.graph


    def node_iterator(self):

        self.graph = {v: set(u for u in neighbors_list if v < u)
                      for v, neighbors_list in self.graph.items()}

        count_triangles = 0
        for v, nbrs_v in tqdm(self.graph.items()):
            for u1, u2 in combinations(nbrs_v, 2):
                if u1 in self.graph[u2] or u2 in self.graph[u1]:
                    count_triangles += 1

        return count_triangles

