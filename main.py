from source.brute_force import BruteForce
from source.node_iterator import NodeIterator
from source.compact_forward import CompactForward
from source.doulion import Doulion
from source.graph_class import Graph
import time

from source.triest import Triest


def main():
    with_doulion = False
    p = 0.8

    # select graph
    graph_path, is_directed, has_triangles = graph_picker("astroph")
    graph = Graph(graph_path)

    # run doulion
    if with_doulion:
        run_with_timer(
            Doulion(p, graph, is_directed).doulion)

    # brute_force = BruteForce(graph, is_directed).brute_force
    # node_iterator = NodeIterator(graph, graph.graph_edges).node_iterator
    # compact_forward = CompactForward(graph).compact_forward
    triest = Triest(graph.graphAsStream(), memorySize=50000).triest

    # run list of algorithms
    for algorithm in [triest]:

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


def graph_picker(graph_name):
    if graph_name == "astroph":
        # undirected https://snap.stanford.edu/data/ca-AstroPh.html
        graph_path = "graphs/CA-AstroPh.txt"
        has_triangles = 1351441
        is_directed = False

    if graph_name == "grqc":
        graph_path = "graphs/CA-GrQc.txt"
        has_triangles = 48260
        is_directed = False

    elif graph_name == "emailcore":
        # directed https://snap.stanford.edu/data/email-Eu-core.html
        graph_path = "graphs/email-Eu-core.txt"
        has_triangles = 105461
        is_directed = True

    elif graph_name == "toyUndirected":
        graph_path = "graphs/toy_example_3_triangles.txt"
        has_triangles = 3
        is_directed = False

    elif graph_name == "toyDirected":
        graph_path = "graphs/toy_example_directed.txt"
        has_triangles = 2
        is_directed = True

    else:
        Exception("Unknown dataset")

    return graph_path, is_directed, has_triangles


if __name__ == '__main__':
    main()