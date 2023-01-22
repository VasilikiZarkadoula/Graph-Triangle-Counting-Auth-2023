import json
import time
from os import mkdir
from os.path import exists

import numpy as np
from random import seed
from matplotlib import pyplot as plt

from source.util import *
from source.brute_force import BruteForce
from source.node_iterator import NodeIterator
from source.compact_forward import CompactForward
from source.doulion import Doulion
from source.triest import Triest
from source.graph_class import Graph

RESULTS_DIR  = 'results/'
TRIEST_ACCURACY_THRS = 99.6
MEMORY_LIMIT = 15000

class RunAlgorithms:
    def __init__(self, args, saved_results_file_path=None):
        """
        :param args: dotdict with the parameters
        :param saved_results_file_path: a file path where the results of a
                previous run are saved. The results are printed. The plots
                are also drawn if multiple iterations of an approx algo ran
                (args.plotApproximate values was True)
        """

        self.results = None
        if saved_results_file_path is not None:
            self.print_saved_results(saved_results_file_path)
        else:
            self.args = args
            self.args.graph_path, self.args.saved_as_directed, self.args.numOfTriangles = \
                graph_picker(self.args.graph_name)
            self.graph = None

            self.setup()
            self.run_iterations()
            self.save_results()
            self.show_results()


    def setup(self):

        if self.args.selected_algorithm == TRIEST:
            self.graph = Graph(self.args.graph_path, self.args.saved_as_directed).graphAsStream()
            start, end, step, self.args.paramName = 1000, len(self.graph), 1000, 'memorySize'

        elif self.args.with_doulion:
            start, end, step, self.args.paramName = 0.1, 1, 0.1, 'p'

        self.args.apprParamValues = \
            np.arange(start, end, step) if self.args.plotApproximate \
            else [self.args.get(self.args.paramName, '')]


    def algorithm_picker(self, selected_algorithm):
        if selected_algorithm == BRUTE_FORCE:
            return BruteForce(self.graph).brute_force

        elif selected_algorithm == NODE_ITERATOR:
            return NodeIterator(self.graph, self.graph.graph_edges).node_iterator

        elif selected_algorithm == COMPACT_FORWARD:
            return CompactForward(self.graph).compact_forward

        elif selected_algorithm == TRIEST:
            return Triest(self.graph, self.args.memorySize).triest

        elif selected_algorithm == DOULION:
            return Doulion(self.args.p, self.graph).doulion

        else:
            Exception(f"Wrong input: {selected_algorithm}")


    def run_iterations(self):
        self.results = {key: [] for key in [f'{DOULION} runtime', f'{self.args.selected_algorithm} runtime',
                                            'Estimated Triangles', 'Accuracy']}

        for approximationParamValue in self.args.apprParamValues:
            self.args[self.args.paramName] = approximationParamValue
            values = self.run_triangle_counting_alg_iteration()

            for i, key in enumerate(self.results):
                self.results[key].append(values[i])

            if self.break_(approximationParamValue):
                self.args.apprParamValues = self.args.apprParamValues[:len(self.results['Accuracy'])]
                break

        if not self.args.with_doulion:
            del self.results[f'{DOULION} runtime']


    def break_(self, approximationParamValue):
        # print current iteration results
        if len(self.args.apprParamValues):
            print(f'\n{self.args.paramName} = {approximationParamValue}')
            [print(f'{key} : {value[-1]}') for key, value in self.results.items()]

        if self.args.selected_algorithm != TRIEST:
            return False

        # if selected algorithm is triest, check break conditions
        if self.results['Accuracy'][-1] == 100:
            return True

        return approximationParamValue > MEMORY_LIMIT and \
            self.results['Accuracy'][-1] > TRIEST_ACCURACY_THRS


    def run_triangle_counting_alg_iteration(self):

        # if algorithm is brute force, node iter or compact load graph
        # else if triest : graph stream already loaded
        if self.args.selected_algorithm != TRIEST:
            self.graph = Graph(self.args.graph_path, self.args.saved_as_directed)

        # if with_doulion == True, pick doulion to sparcify the graph and calculate runtime
        doulion_runtime = self.run_with_timer(
            self.algorithm_picker(DOULION)
        )[1] if self.args.with_doulion else None

        # pick and run selected algorithm to calculate number of triangles
        estimated_triangles, alg_runtime = self.run_with_timer(
            self.algorithm_picker(self.args.selected_algorithm)
        )
        # if doulion ran, correct the number of estimated triangles
        if self.args.with_doulion:
            estimated_triangles *= 1 / self.args.p ** 3

        # calculate estimation accuracy
        accuracy = self.accurary(estimated_triangles)

        return doulion_runtime, alg_runtime, int(estimated_triangles), accuracy


    def run_with_timer(self, algorithm):
        start = time.time()
        result = algorithm()
        end = time.time()
        return result, end - start


    def accurary(self, estimated_triangles):
        return 100 - (abs(estimated_triangles - self.args.numOfTriangles) / self.args.numOfTriangles) * 100.0


# ============================================================================================================
# Print, plot and save results :
# ============================================================================================================


    def show_results(self):
        if self.args.plotApproximate:
            self.plotApproximate()
        else:
            [print(f'{key} : {value[0]}') for key, value in self.results.items()]

    def save_results(self):
        if not exists(RESULTS_DIR[:-1]):
            mkdir(RESULTS_DIR[:-1])
        file_name = f"{RESULTS_DIR}{self.args.graph_name}_alg-{self.args.selected_algorithm}_doulion-{self.args.with_doulion}_{str(time.time())[-5:]}.json"

        with open(file_name, 'w') as file:
            # turn int32 args to strings to avoid not json serializable exception
            self.args.memorySize = str(self.args.memorySize)
            self.args.apprParamValues = [str(v) for v in list(self.args.apprParamValues)]
            json.dump({'args': self.args, 'results': self.results}, file, indent=4)

    def print_saved_results(self, saved_results_file_path):
        print('\nFILE RESULTS:', saved_results_file_path)

        with open(saved_results_file_path, 'r') as file:
            data = json.load(file)
        self.args = dotdict(data['args'])
        self.results = data['results']
        self.args.toString()
        self.show_results()


    def plotApproximate(self):

        color = ['tab:blue', 'tab:cyan', 'tab:green', 'tab:orange']
        plt.style.use(plt.style.library['seaborn-whitegrid'])

        class_ = int if self.args.paramName == 'memorySize' else float
        x = [class_(i) for i in self.args.apprParamValues]
        xlabel = self.args.paramName

        fig, axs = plt.subplots(nrows=len(self.results), ncols=1, figsize=(7, 10), squeeze=True)
        plt.rcParams.update({'font.size': 12})
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        for i, (label, values) in enumerate(self.results.items()):
            print(label, values)
            axs[i].plot(x, values, color=color[i])
            axs[i].set_xticks(x)
            axs[i].set(xlabel=xlabel, ylabel=label)

        plt.show()


# ============================================================================================================


def main():
    seed(42)
    args = dotdict({})

    # set arguments:

    # Selected dataset (as a variable, not str) for graph_picker
    # (see available graphs at util.py)
    args.graph_name = ASTROPH

    # BRUTE_FORCE, NODE_ITERATOR, COMPACT_FORWARD or TRIEST (as a variable not str, capital)
    args.selected_algorithm = COMPACT_FORWARD

    # Sparcify graph? True or False
    args.with_doulion = True
    # Doulion approximation parameter: Coin toss success probability. 0 <= p <= 1
    args.p = 0.1

    # Triest approximation parameter: sample size (# sampled edges). Integer
    args.memorySize = 3000

    # Run multiple iteration of an approximation alg with incremental approx param values
    # and plot results (for Doulion or Triest)? True or False
    # if True default approx param value is ignored
    args.plotApproximate = False

    validate_args(args)
    # print args:
    args.toString()

    # Uncomment to run algorithm according to args
    RunAlgorithms(args)

    # load results from file (pycharm autocompletes). Uncomment to run
    saved_results_file_path = 'results/CA-GrQc_alg-Brute Force_doulion-False_60584.json'
    # RunAlgorithms(None, saved_results_file_path)


if __name__ == '__main__':
    main()
