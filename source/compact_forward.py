
class NeighborsIterator:
    def __init__(self, neighbors):
        self.neighbors = neighbors
        self.i = 0

    def has_next(self):
        return self.i < len(self.neighbors)

    def next(self):
        try:
            node = self.neighbors[self.i]
            self.i += 1
        except IndexError:
            node = None
        return node


class CompactForward:
    # TODO : check directed graphs

    def __init__(self, graph, with_duolion = False):
        self.graph = graph
        self.triangle_value = 1 / 3 if with_duolion else 1
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
        self.sort_nodes(nodes, for_nodes=True)  # 1

        for v in nodes:     # 2
            self.sort_nodes(self.graph.neighbors(v))

        for v in nodes:     # 3
            for u in self.graph.neighbors(v):   # 3a
                if self.order[u] > self.order[v]:

                    Nu = NeighborsIterator(self.graph.neighbors(u))
                    Nv = NeighborsIterator(self.graph.neighbors(v))

                    # 3aa
                    u_ = Nu.next()   # u'
                    v_ = Nv.next()   # v'

                    if u_ is None:   # u has no outgoing edges
                        break

                    while Nu.has_next() and Nv.has_next():                    # 3ab1
                        if self.order[v_] < self.order[v] > self.order[u_]:   # 3ab2

                            if self.order[u_] < self.order[v_]:               # 3aba
                                u_ = Nu.next()
                            elif self.order[u_] > self.order[v_]:             # 3abb
                                v_ = Nv.next()
                            else:                                             # 3abc
                                count_triangles += self.triangle_value
                                #print(u, v, u_)
                                u_ = Nu.next()
                                v_ = Nv.next()
                        else:
                            break
        return count_triangles

