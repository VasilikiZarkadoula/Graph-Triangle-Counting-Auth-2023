class BruteForce:

    def __init__(self, graph, with_duolion = False, is_directed = False):
        self.graph = graph
        self.triangle_value = 1 / 3 if with_duolion else 1
        self.denominator = 3 if is_directed else 6
        self.order = None

    def brute_force(self):
        adj = self.graph.adj_matrix()
        nodes = len(adj)
        count_triangle = 0

        for i in range(nodes):
            for j in range(nodes):
                for k in range(nodes):

                    # check the triplet
                    # if it satisfies the condition
                    if (i != j and i != k
                            and j != k and
                            adj[i][j] and adj[j][k]
                            and adj[k][i]):
                        count_triangle += 1

        # If graph is directed , division is done by 3
        # else division by 6 is done

        return count_triangle // self.denominator



