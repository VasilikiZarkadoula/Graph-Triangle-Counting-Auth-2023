import json
import time
from os import mkdir
from os.path import exists

import numpy as np

from other.plot_results import PlotResults
from other.util import *
from algorithms.brute_force import BruteForce
from algorithms.node_iterator import NodeIterator
from algorithms.compact_forward import CompactForward
from algorithms.doulion import Doulion
from algorithms.triest import Triest
from other.graph_class import Graph

RESULTS_DIR  = 'results/'

class RunAlgorithms:
    def __init__(self, args):
        self.graph = None
        self.results = None

        self.args = args
        self.args.graph_path, self.args.saved_as_directed, self.args.numOfTriangles = graph_picker(self.args.graph_name)

        self.setup()
        self.run_iterations()
        self.save_results()
        PlotResults(self.args, self.results)


    def setup(self):

        if self.args.selected_algorithm == TRIEST:
            self.graph = Graph(self.args.graph_path, self.args.saved_as_directed, triest=True).graph
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
            return NodeIterator(self.graph).node_iterator

        elif selected_algorithm == COMPACT_FORWARD:
            return CompactForward(self.graph).compact_forward

        elif selected_algorithm == TRIEST:
            return Triest(self.graph, self.args.memorySize).triest

        elif selected_algorithm == DOULION:
            return Doulion(self.args.p, self.graph).doulion

        else:
            Exception(f"Wrong input: {selected_algorithm}")

# ============================================================================================================

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

        return approximationParamValue > self.args.triestBreakMemoryLimit


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

    def save_results(self):
        if not exists(RESULTS_DIR[:-1]):
            mkdir(RESULTS_DIR[:-1])
        file_name = f"{RESULTS_DIR}{self.args.graph_name}_alg-{self.args.selected_algorithm}_doulion-{self.args.with_doulion}_{str(time.time())[-5:]}.json"

        with open(file_name, 'w') as file:
            # turn int32 args to strings to avoid not json serializable exception
            self.args.memorySize = str(self.args.memorySize)
            self.args.apprParamValues = [str(v) for v in list(self.args.apprParamValues)]
            json.dump({'args': self.args, 'results': self.results}, file, indent=4)


# ============================================================================================================


