from source.brute_force import BruteForce
from source.compact_forward import CompactForward
from source.graph_class import Graph
import time

# https://snap.stanford.edu/data/ca-AstroPh.html
# undirected
# graph_path = "graphs/toy_example_3_triangles.txt"

# directed
# graph_path = "graphs/email-Eu-core.txt"
graph_path = "graphs/toy_example_directed.txt"

def main():
    graph = Graph(graph_path)
    print(graph)
    with_doulion = False
    is_directed = True

    #compact_forward = CompactForward(graph, with_doulion).compact_forward
    brute_force = BruteForce(graph, with_doulion, is_directed).brute_force

    for algorithm in [brute_force]:
        print(algorithm.__name__)
        start = time.time()
        triangles = algorithm()
        end = time.time()

        print(f'\t# triangles = {triangles}')
        print(f'\telapsed time = {end - start}')

if __name__ == '__main__':
    main()
