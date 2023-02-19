from random import seed

from other.util import *
from other.run_algorithm import RunAlgorithms


def SET_ARGUMENTS():
    """
    This function can be used to set the arguments that will be used for the execution of the triangle
    counting algorithm. These include the selected algorithm and graph dataset name. Whether the graph
    will be sparsified before its triangles are counted and the probability p of maintaining each edge.
    In case the selected algorithm is Triest, the memory size (max # edges in the sample) can be set
    instead.
    If the selected algorithm is approximate, its performance can be compared for different
    values of the approximation parameter (p or memorySize) through plots generated from multiple
    runs of the algorithm. For Triest : To limit the memory size to a desired range(1k, limit, 1k)
    set the value of the triestBreakMemoryLimit accordingly.
    The argument values set will then be validated and appropriate messages will be
    printed to assist the user select values for the desired configuration.
    After the execution is finished, the results will be printed in the command line and, if
    plotApproximate is set to True, plots will also be shown (note that if the algorithm is exact
    plots will not show up despite plotApproximate being set to True).
    The results will also be saved in an appropriately named json file inside the '/results' folder.
    Results reported in the paper are saved in '/results/archived_results'. To plot past saved results
    refer to '/other/plot_results.py'.
    """
    args = dotdict({})
    # Random seed value
    seed(42)

    # Selected dataset as a variable, not str (see available graphs at other\util.py)
    # Currently available :
    # GRQC (Small), ASTROPH (Medium), YOUTUBE (Large Dense), SPARSE_ROADS (Large Sparse)
    args.graph_name = GRQC

    # BRUTE_FORCE, NODE_ITERATOR, COMPACT_FORWARD or TRIEST (as a variable not str, capital)
    args.selected_algorithm = NODE_ITERATOR

    # Sparsify graph? True or False
    args.with_doulion = True
    # Doulion approximation parameter: Coin toss success probability. 0 <= p <= 1
    args.p = 0.1

    # Triest approximation parameter: sample size (# sampled edges). Integer
    args.memorySize = 3000
    # Limit the executions of Triest when plotApproximate is set to True
    # Set to a greater value than the number of edges to plot for memorySize in range(1k, #edges, 1k)
    args.triestBreakMemoryLimit = 40000

    # Run multiple runs of an approximation alg with incremental approx param values
    # and plot results (for Doulion or Triest)? True or False
    # if True default approx param value is ignored
    args.plotApproximate = True

    return args


# ==========================================================================================
def main():
    # The arguments that will be used for the execution of the selected algorithm
    args = SET_ARGUMENTS()
    validate_args(args)
    # print args:
    args.toString()
    # run algorithm according to args
    RunAlgorithms(args)


if __name__ == '__main__':
    main()
