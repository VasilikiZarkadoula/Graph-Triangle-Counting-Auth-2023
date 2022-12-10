import random


class Doulion:
    def __init__(self, p, graph, is_directed):
        self.p = p
        self.graph = graph
        self.undirected = not is_directed
        self.toDel = None

    def doulion(self):
        if self.undirected:
            # node v : list of neighbors u to be removed (v < u)
            self.toDel = {}
            # 2 steps for undirected. time compl Θ(2*m)
            steps = [self.undirected_toss_coins,
                     self.undirected_sparsify]
        else:
            # 1 step for directed. time compl Θ(m)
            steps = [self.directed_sparsify]
        for step in steps:
            self.run_step(step)


    def run_step(self, step):
        for v, neighbors in self.graph.graph.items():
            step(v, neighbors)


    def undirected_toss_coins(self, v, neighbors):
        """
        Step 1 for undirected: Toss coins for edges (u,v)=(v,u)
        1. For u in v's neighbors list:
           2. Toss the coin once for each undirected edge (only for (1,2), not (2,1))
           3. If failure (v,u) (and its inverse (u,v)) will be removed
        """
        self.toDel[v] = {
            u for u in neighbors if u > v and self.failure_coin()
        }


    def undirected_sparsify(self, v, neighbors):
        """
        Step 2 for undirected:
        For each node v, adj list = neighbors u : coin toss (v,u) (when u>v)
                                                         or (u,v) (when v>u) not a failure """
        self.graph.set_neighbors(v,
                # 0.04 sec faster:
                [u for u in neighbors if (u > v and u not in self.toDel[v]) or (v > u and v not in self.toDel[u])]
                # [u for u in neighbors if (u not in self.toDel[v]) and (v not in self.toDel[u])]
        )

    def directed_sparsify(self, v, neighbors):
        # For each node v, adj list = neighbors u whose coin toss isn't a failure
        self.graph.set_neighbors(v,
                                 [u for u in neighbors if not self.failure_coin()])

    def failure_coin(self):
        return random.random() > self.p


