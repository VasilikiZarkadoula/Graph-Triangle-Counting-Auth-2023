from random import randint, random


class GraphSample:
    def __init__(self, memorySize):
        self.memorySize = memorySize
        self.edges = []
        self.sample = {}

    def memoryFull(self):
        return len(self.edges) == self.memorySize

    def neighborsInSample(self, v):
        return self.sample.get(v, set())

    def _insertEdge(self, v, u):
        for node, neighbor in [(v, u), (u, v)]:
            try:
                self.sample[node].add(neighbor)
            except KeyError:
                self.sample[node] = {neighbor}

    def _deleteEdge(self, v, u):
        for node, neighbor in [(v, u), (u, v)]:
            self.sample[node].remove(neighbor)
            if len(self.sample[node]) == 0:
                del self.sample[node]

    def insertToSample(self, v, u):
        if v in self.sample and u in self.sample[v]:
            return
        if self.memoryFull():
            toBeReplacedIndex = randint(0, self.memorySize - 1)
            v_replace, u_replace = self.edges[toBeReplacedIndex]
            self.edges[toBeReplacedIndex] = (v, u)
            self._deleteEdge(v_replace, u_replace)
        else:
            self.edges.append((v, u))
        self._insertEdge(v, u)



class Triest:

    def __init__(self, graphStream, memorySize):
        self.t = 0
        self.memorySize = memorySize
        self.graphStream = graphStream
        self.count_global_triangles = 0
        self.sample = GraphSample(memorySize)


    def triest(self):
        for v, u in self.graphStream :
            if v < u:
                self.t += 1
                self._updateCounters(v, u)
                if self._sampleStreamEdge():
                    self.sample.insertToSample(v, u)
        return self.count_global_triangles


    def _updateCounters(self, v, u):

        weight = ((self.t - 1) * (self.t - 2)) / \
                 (self.memorySize * (self.memorySize - 1))
        weight = max(1., weight)

        numOfCommonNeighbors = \
            len(self.sample.neighborsInSample(v).intersection(self.sample.neighborsInSample(u)))

        self.count_global_triangles += weight * numOfCommonNeighbors


    def _sampleStreamEdge(self):
        return not self.sample.memoryFull() or self._coinSuccess()

    def _coinSuccess(self):
        return random() <= self.memorySize / self.t
