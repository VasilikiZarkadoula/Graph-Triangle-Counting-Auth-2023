import json
from os.path import exists
from matplotlib import pyplot as plt
from other.util import dotdict
class PlotResults:

    def __init__(self, args=None, results=None, file_path=None):
        """
          :param args: dotdict with the parameters. Leave None to print file results
          :param results dict of results. Leave None to print file results
          :param saved_results_file_path: a file path where the results of a
                  previous run are saved. The results are printed. The plots
                  are also drawn if multiple iterations of an approx algo ran
                  (args.plotApproximate values was True)
        """
        if file_path is not None and exists(file_path):
            self.load_seved_results(file_path)
        else:
            self.args = args
            self.results = results

        self.show_results()

    def load_seved_results(self, file_path):
        print('\nFILE RESULTS:', file_path)

        with open(file_path, 'r') as file:
            data = json.load(file)
        self.args = dotdict(data['args'])
        self.results = data['results']
        self.args.toString()

    def show_results(self):
        if self.args.plotApproximate:
            self.plotApproximate()
        else:
            [print(f'{key} : {value[0]}') for key, value in self.results.items()]

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


if __name__ == '__main__':
    # load results from file (pycharm autocompletes). Uncomment to run
    saved_results_file_path = '../results/com-youtube.ungraph_alg-Compact Forward_doulion-True_72483.json'
    PlotResults(file_path=saved_results_file_path)