
class NeighborsIterator:
    def __init__(self, neighbors):
        self.neighbors = neighbors
        self.i = -1

    def has_next(self):
        return self.i < len(self.neighbors)

    def next(self):
        try:
            self.i += 1
            node = self.neighbors[self.i]
        except IndexError:
            node = None
        return node


class CompactForward:

    def __init__(self, graph):
        self.graph = graph
        self.order = None

    def degree_order(self):
        # node v : order = degree(v)
        return {v: self.graph.degree(v) for v in self.graph.nodes()}

    def sort_nodes(self, nodes, for_nodes=False):
        # sort nodes by degree -descending-  d(0) > d(1) > ... > d(n)
        # order(v) < order(u) <=> d(v) > d(u) or (d(v) == d(u) and v < u)

        # sort neighbors by order -ascending- o(0) < o(1) < ... < o(m)
        nodes.sort(key=lambda v: (self.order[v], -v), reverse=for_nodes)
        if for_nodes:
            self.order = {v : i for i, v in enumerate(nodes)}


    def compact_forward(self):

        count_triangles = 0
        nodes = self.graph.nodes()
        self.order = self.degree_order()
        #print(self.order)
        self.sort_nodes(nodes, for_nodes=True)  # 1

        for v in nodes:     # 2
            self.sort_nodes(self.graph.neighbors(v))

        #print(self.order)

        for v in nodes:     # 3
            #print('v=', v, self.order[v])
            for u in self.graph.neighbors(v):   # 3a
                #print('\tu=', u, self.order[u])
                if self.order[u] > self.order[v]:

                    Nu = NeighborsIterator(self.graph.neighbors(u))
                    Nv = NeighborsIterator(self.graph.neighbors(v))

                    #print('\tNu =', Nu.neighbors); print('\tNv=', Nv.neighbors)

                    # 3aa
                    u_ = Nu.next()   # u'
                    v_ = Nv.next()   # v'

                    #print(f"\t\tv'= {v_}  {self.order[v_]}")
                    #print(f"\t\tu'= {u_}  {self.order[u_]}")

                    while Nu.has_next() and Nv.has_next():                    # 3ab1
                        if self.order[v_] < self.order[v] > self.order[u_]:   # 3ab2

                            if self.order[u_] < self.order[v_]:               # 3aba
                                u_ = Nu.next()
                            elif self.order[u_] > self.order[v_]:             # 3abb
                                v_ = Nv.next()
                            else:                                             # 3abc
                                #print('TRIANGLE ', v, u, u_)
                                count_triangles += 1
                                u_ = Nu.next()
                                v_ = Nv.next()

                            #print(f"\t\tv'= {v_}  {self.order[v_]}")
                            #print(f"\t\tu'= {u_}  {self.order[u_]}")

                        else:
                            #print("BREAK")
                            break
        return count_triangles


