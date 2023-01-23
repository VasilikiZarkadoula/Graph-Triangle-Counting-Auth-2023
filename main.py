from source.brute_force import BruteForce
from source.node_iterator_version2 import NodeIterator
from source.compact_forward import CompactForward
from source.doulion import Doulion
from source.graph_class import Graph
import time

from source.triest import Triest
from source.util import *


def main():
    with_doulion = False
    p = 0.1

    # select graph
    # saved_as_directed = True if only (v,u) is included in the file, not its symmetric (u,v)
    graph_path, saved_as_directed, has_triangles = graph_picker(YOUTUBE)
    graph = Graph(graph_path, saved_as_directed, triest=False)

    # run doulion
    if with_doulion:
        run_with_timer(
            Doulion(p, graph).doulion)

    # brute_force = BruteForce(graph).brute_force
    node_iterator = NodeIterator(graph).node_iterator
    # compact_forward = CompactForward(graph).compact_forward
    # triest = Triest(graph.graph, memorySize=50000).triest

    # run list of algorithms
    for algorithm in [node_iterator]:

        triangles = run_with_timer(algorithm)
        if with_doulion:
            triangles *= 1 / p**3

        accuracy = 100 - (abs(triangles - has_triangles) / has_triangles) * 100.0
        print(f'\t# triangles = {int(triangles)}\n\taccuracy = {accuracy}')


def run_with_timer(algorithm):
    print(algorithm.__name__)
    start = time.time()
    result = algorithm()
    end = time.time()
    print(f'\telapsed time = {end - start}')
    return result



if __name__ == '__main__':
    main()