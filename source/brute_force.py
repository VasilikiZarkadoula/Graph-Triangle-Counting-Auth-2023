from tqdm import tqdm


class BruteForce:

    def __init__(self, graph, is_directed = False):
        self.graph = graph
        # self.denominator = 3 if is_directed else 6

    def brute_force(self):
        adj = self.graph.adj_matrix()
        nodes = len(adj)
        count_triangle = 0

        for i in tqdm(range(nodes)):
            for j in range(i + 1, nodes):
                for k in range(j + 1, nodes):

                    # check the triplet
                    # if it satisfies the condition
                    if adj[i][j] and adj[j][k] and adj[k][i]:
                        count_triangle += 1

        # If graph is directed , division is done by 3
        # else division by 6 is done

        return count_triangle  # // self.denominator



