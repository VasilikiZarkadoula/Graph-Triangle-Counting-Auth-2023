from source.compact_forward import CompactForward
from source.graph_class import Graph
import time

# https://snap.stanford.edu/data/ca-AstroPh.html
# undirected
graph_path = "graphs/CA-AstroPh.txt"

# directed
# graph_path = "graphs/email-Eu-core.txt"


def main():
    graph = Graph(graph_path)
    with_doulion = False

    compact_forward = CompactForward(graph, with_doulion).compact_forward

    for algorithm in [compact_forward]:
        print(algorithm.__name__)
        start = time.time()
        triangles = algorithm()
        end = time.time()

        print(f'\t# triangles = {triangles}')
        print(f'\telapsed time = {end - start}')


if __name__ == '__main__':
    main()

