import numpy as np
import matplotlib.pyplot as plt
from plotCDF.discrete import systems


class PMF:
    def __init__(self, support, probabilities, tol=.1e-12):
        self.string = ''
        self.cdf = np.nan
        s = np.asarray(support)
        p = np.asarray(probabilities, dtype=np.float64)
        if s.ndim != 1:
            self.string = 'the support should be one dimensional'
        elif p.ndim != 1:
            self.string = 'the probabilities should be one dimensional'
        elif s.size != p.size:
            self.string = 'both support and probabilities should have the same size'
        elif sum(p <= 0) > 0:
            self.string = 'all probabilities should be greater than zero'
        elif np.abs(sum(p) - 1.) > tol:
            self.string = 'the probabilities should sum 1 and not ' + str(sum(p))
        else:
            pass

        if not self.string:
            self.support = s
            self.probabilities = p
            self.cdf = np.cumsum(p)
            self.tol = tol
        else:
            print(self.string)

    def graph(self, rv_name='X', graph_name=''):
        fig, ax = plt.subplots()
        # plt.bar(self.support, self.probabilities, width=.1, color='b')
        plt.plot(self.support, self.probabilities, 'ko--')
        plt.title('Função de Probabilidade da v.a. ' + rv_name.upper())
        plt.xlabel(rv_name.lower())
        plt.ylabel('P(' + rv_name.upper() + '=' + rv_name.lower() + ')')
        if self.support.size <= 10:
            ax.set_xticks(self.support)
            ax.set_yticks(self.probabilities)
        plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
        file_name = graph_name + '_pmf_' + rv_name + '.eps'
        if systems.is_windows():
            manager = plt.get_current_fig_manager()
            manager.window.showMaximized()
            plt.tight_layout()
        plt.savefig(file_name, format='eps', dpi=3600)
        # plt.show()
        return ax


class CDF:
    def __init__(self, support, probabilities, tol=.1e-12):
        self.string = ''
        s = np.asarray(support)
        p = np.asarray(probabilities, dtype=np.float64)
        dif = np.diff(p)
        if s.ndim != 1:
            self.string = 'the support should be one dimensional'
        elif p.ndim != 1:
            self.string = 'the probabilities should be one dimensional'
        elif s.size != p.size:
            self.string = 'both support and probabilities should have the same size'
        elif sum(dif < 0) > 0:  # note that due to generated error we use <0
            self.string = 'all probabilities should be greater than zero, so all increments must be positive'
        elif np.abs(p[-1] - 1.) > tol:
            self.string = 'the probabilities should sum 1 and not ' + str(p[-1])
        else:
            pass

        if not self.string:
            self.support = s
            self.probabilities = p
            self.pmf = np.insert(np.diff(p), 0, p[0])
            self.tol = tol
        else:
            print(self.string)

    def graph(self, rv_name='X', graph_name=''):
        # we need to sort the support and the probabilities accordingly

        ext_support = np.append(self.support, self.support[-1] + (self.support[-1] - self.support[0]) * .1)
        ext_support = np.insert(ext_support, 0, self.support[0] - (self.support[-1] - self.support[0]) * .1)
        # ext_probabilities = np.append(self.probabilities, 1)
        ext_probabilities = np.insert(self.probabilities, 0, 0)

        fig, ax = plt.subplots()
        ax.plot(ext_support[1], ext_probabilities[0], 'o', markerfacecolor='white', markeredgecolor='black')
        ax.hlines(y=ext_probabilities[0], xmin=ext_support[0], xmax=ext_support[1], linestyle='dashed',
                  linewidth=2, color='k')
        ax.hlines(y=1, xmin=ext_support[ext_support.size - 2], xmax=ext_support[ext_support.size - 1],
                  linestyle='dashed',
                  linewidth=2, color='k')
        for x in range(1, ext_support.size - 2):
            ax.plot(ext_support[x], ext_probabilities[x], 'ko')
            ax.plot(ext_support[x + 1], ext_probabilities[x], 'o', markerfacecolor='white', markeredgecolor='black')
            ax.hlines(y=ext_probabilities[x], xmin=ext_support[x], xmax=ext_support[x + 1], linewidth=2, color='k')
        plt.plot(ext_support[ext_support.size - 2], ext_probabilities[ext_support.size - 2], 'ko')
        plt.title('Função de Distribuição da v.a. ' + rv_name.upper())
        plt.xlabel(rv_name.lower())
        plt.ylabel('F(' + rv_name.lower() + ')')
        if self.support.size <= 10:
            ax.set_xticks(self.support)
            ax.set_yticks(self.probabilities)
        plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
        if systems.is_windows():
            manager = plt.get_current_fig_manager()
            manager.window.showMaximized()
            plt.tight_layout()
        file_name = graph_name + '_cdf_' + rv_name + '.eps'
        plt.savefig(file_name, format='eps', dpi=3600)
        # plt.show()
        return ax


def expected_value(pmf, function):
    function_values = function(pmf.support)
    return np.dot(function_values, pmf.probabilities)


def expected_value_x_power_k(pmf, k=1):
    return np.dot(np.power(pmf.support, k), pmf.probabilities)


def expected_value_x2(pmf):
    return expected_value_x_power_k(pmf, 2)


def variance_x(pmf):
    return expected_value_x_power_k(pmf, 2) - expected_value_x_power_k(pmf) ** 2


def std_dev_x(pmf):
    return variance_x(pmf) ** .5


def is_well_formatted(string):
    if not string:
        return True
    else:
        return False


""""
    def check(self):
        if self.support.ndim != 1: return 'the support should be one dimensional'
        if self.probabilities.ndim != 1: return 'the probabilities should be one dimensional'
        if self.support.size != self.probabilities.size: return 'both support and probabilities should have ' \
                                                                'the same size'
        if sum(self.probabilities <= 0) > 0: return 'all probabilities should be greater than zero'
        if sum(self.probabilities) != 1: return 'the probabilities should sum 1'
        return True
"""
