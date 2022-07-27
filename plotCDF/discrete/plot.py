# This script allows us to prepare the data so we can plot beautiful graphics for discrete random variables.


from plotCDF.discrete import checks
import numpy as np
import matplotlib.pyplot as plt
from plotCDF.library import systems
import logging


class RV:
    '''
    We use the class to instantiate a discrete random variable, so we can make beautiful plots for the
    point mass function (pmf) but more specifically to the cumulative distribution function (cdf) and the
    quantile (percentile) function.

    :param support: The part of the support of the discrete random variable that we want to plot, that is, the mass points that we will be using. You should pass any type that can be converted to a numpy array and increasingly ordered.
    :param prob: The probability or the cumulative probability for each mass point in the support that we will be using. You should pass any type that can be converted to a numpy array.
    :param is_pmf: A boolean stating if in prob you are passing the pmf or the cdf. By default it's True, so you'll be passing the pmf.
    :param complete_left: A boolean to state if the left tail is complete, that is, if the first mass point in the support is the minimum mass point for this discrete random variable. By default it's True.
    :param complete_right: A boolean to state if the right tail is complete, that is, if the last mass point in the support is the maximum mass point for this discrete random variable. By default it's True.
    :param max_tol: A tolerance value so you can check if the sum of the probabilities are equal to 1 or not. If not, you'll get a warning. A default float of 1e-12.
    '''

    def __new__(cls, support, prob, is_pmf=True, complete_left=True, complete_right=True, max_tol=1e-12):
        messages = []

        if not is_pmf:
            try:
                p = np.array(prob)
                prob = np.append(p[0], p[1:] - p[:-1])
            except TypeError as e:
                messages.append('We need a type that can be converted to a numpy array. ' + str(e))

        try:
            checks.support(support)
        except(ValueError, TypeError) as e:
            messages.append(e)

        try:
            checks.prob(prob, max_tol)
        except(ValueError, TypeError) as e:
            messages.append(e)

        try:
            checks.comp_supp_prob(support, prob)
        except TypeError as e:
            messages.append(e)

        try:
            checks.tolerance(max_tol)
        except ValueError as e:
            messages.append(e)

        try:
            checks.tail(complete_left)
        except TypeError as e:
            messages.append(e)

        try:
            checks.tail(complete_right)
        except TypeError as e:
            messages.append(e)

        try:
            checks.is_pmf(is_pmf)
        except TypeError as e:
            messages.append(e)

        if not messages:
            return object.__new__(cls)
        else:
            logging.critical(messages)
            return None

    def __init__(self, support, prob, is_pmf=True, complete_left=True, complete_right=True, max_tol=1e-12):
        self.support = support
        self.__tol = max_tol
        self.__is_pmf = is_pmf
        self.prob = prob
        self.__warning = checks.is_sum_probs_tol(self.prob, max_tol)
        if self.is_pmf:
            self.__cum_prob = self.from_pmf_to_cdf(self.prob)
        else:
            self.__cum_prob = prob
        self.complete_left = complete_left
        self.complete_right = complete_right
        if self.__warning:
            logging.warning(self.__warning)

    def __str__(self) -> str:
        msg = 'A discrete Point Mass Function: ' + self.__repr__()
        # return super().__str__()
        return msg

    def __repr__(self) -> str:
        msg = "{}({}, {}, {}, {}, {}, {})".format(self.__class__.__name__, self.__support, self.__prob,
                                                  self.__is_pmf, self.complete_left, self.complete_right, self.tol)
        # return super().__repr__()
        return msg

    @property
    def warning(self):
        return self.__warning

    @property
    def support(self):
        return self.__support

    @support.setter
    def support(self, s):
        s = checks.support(s)
        try:
            p = self.prob
            try:
                checks.comp_supp_prob(s, p)
                self.__support = s
            except (ValueError, TypeError) as e:
                print(e)
        except AttributeError as e:
            self.__support = s

    @property
    def is_pmf(self):
        return self.__is_pmf

    @property
    def prob(self):
        return self.__prob

    @prob.setter
    def prob(self, p):
        if not self.is_pmf:
            p = self.from_cdf_to_pmf(p)
        checks.support(p)
        try:
            checks.prob(p, self.tol)
        except(ValueError, TypeError) as e:
            print(e)
            return
        try:
            s = self.support
            try:
                checks.comp_supp_prob(s, p)
                self.__prob = p
            except (ValueError, TypeError) as e:
                print(e)
        except AttributeError as e:
            self.__prob = p

    @property
    def cum_prob(self):
        return self.__cum_prob

    @property
    def tol(self):
        return self.__tol

    @property
    def complete_left(self):
        return self.__complete_left

    @complete_left.setter
    def complete_left(self, t):
        try:
            checks.tail(t)
            self.__complete_left = t
        except TypeError as e:
            print(e)

    @property
    def complete_right(self):
        return self.__complete_right

    @complete_right.setter
    def complete_right(self, t):
        try:
            checks.tail(t)
            self.__complete_right = t
        except TypeError as e:
            print(e)

    @staticmethod
    def from_pmf_to_cdf(probs):
        '''
        Converts a point mass function (pmf) to a cumulative distribution function (cdf).

        :param probs: The probabilities, that should be positive and with a sum smaller or equal to 1.

        :return: A numpy array with the pmf.
        '''
        probs = np.array(probs)
        return np.cumsum(probs)

    @staticmethod
    def from_cdf_to_pmf(cum_probs):
        '''
        Converts a cumulative distribution function (cdf) to a point mass function (pmf).

        :param cum_probs: The cumulative probabilities, that should be positive, increasing and with a maximum smaller or equal to 1.

        :return: A numpy array with the cdf.
        '''
        cum_probs = np.array(cum_probs)
        return np.append(cum_probs[0], cum_probs[1:] - cum_probs[:-1])

    def plot_cdf(self, rv_name='X', graph_name='', left_points=dict(), right_points=dict(), hlines=dict(),
                 left_line_complete=dict(), right_line_complete=dict(),
                 left_line_incomplete=dict(), right_line_incomplete=dict(),
                 grid=dict(), x_y_ticks=10, save=True):
        '''
        The method used to plot the cumulative distribution function.

        :param rv_name: The name that will appear in the title.
        :param graph_name: the graph's name used to save the file
        :param left_points: A dictionary so you can pass whatever parameters to the left points in the plots.
        :param right_points: A dictionary so you can pass whatever parameters to the right points in the plots.
        :param hlines: A dictionary so you can pass whatever parameters to horizontal lines in the plots.
        :param left_line_complete: A dictionary so you can pass whatever parameters to the left (the first) line in the case the left tail is complete.
        :param right_line_complete: A dictionary so you can pass whatever parameters to the right line (the last) in the case the left tail is complete.
        :param left_line_incomplete: A dictionary so you can pass whatever parameters to the left (the first) line in the case the left tail is incomplete.
        :param right_line_incomplete: A dictionary so you can pass whatever parameters to the right line (the last) in the case the left tail is incomplete.
        :param grid: A dictionary so you can pass whatever parameters to the grid's design.
        :param x_y_ticks: The number of axis x and axis y thicks that you want to use. If the number passed is below the supports's cardinality the default will be used. This is necessary or you'll end up with a graph to much populated in the axis and difficult to read.
        :param save: If you want to save the graph plotted. By default will save an png file, but you can always change it by calling the figure returned (see :return below).

        :return: A tuple with the figure and the plot.
        '''
        increment = np.average(np.diff(self.__support))
        ext_support = np.append(self.__support, self.__support[-1] + increment)
        ext_support = np.insert(ext_support, 0, self.__support[0] - increment)
        ext_probabilities = np.insert(self.__cum_prob, 0, 0)

        fig, ax = plt.subplots()
        if 'markerfacecolor' not in left_points:
            left_points['markerfacecolor'] = 'black'
        if 'markeredgecolor' not in left_points:
            left_points['markeredgecolor'] = 'black'
        if 'marker' not in left_points:
            left_points['marker'] = 'o'

        if 'markerfacecolor' not in right_points:
            right_points['markerfacecolor'] = 'white'
        if 'markeredgecolor' not in right_points:
            right_points['markeredgecolor'] = 'black'
        if 'marker' not in right_points:
            right_points['marker'] = 'o'

        if 'linestyle' not in left_line_complete:
            left_line_complete['linestyle'] = 'dashed'
        if 'linewidth' not in left_line_complete:
            left_line_complete['linewidth'] = 2
        if 'color' not in left_line_complete:
            left_line_complete['color'] = 'k'

        if 'linestyle' not in right_line_complete:
            right_line_complete['linestyle'] = 'dashed'
        if 'linewidth' not in right_line_complete:
            right_line_complete['linewidth'] = 2
        if 'color' not in right_line_complete:
            right_line_complete['color'] = 'k'

        if 'linestyle' not in left_line_incomplete:
            left_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in left_line_incomplete:
            left_line_incomplete['linewidth'] = 2
        if 'color' not in left_line_incomplete:
            left_line_incomplete['color'] = 'r'

        if 'linestyle' not in right_line_incomplete:
            right_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in right_line_incomplete:
            right_line_incomplete['linewidth'] = 2
        if 'color' not in right_line_incomplete:
            right_line_incomplete['color'] = 'r'

        if 'linewidth' not in hlines:
            hlines['linewidth'] = 2
        if 'color' not in hlines:
            hlines['color'] = 'k'

        if 'which' not in grid:
            grid['which'] = 'both'
        if 'axis' not in grid:
            grid['axis'] = 'both'
        if 'color' not in grid:
            grid['color'] = 'grey'
        if 'linestyle' not in grid:
            grid['linestyle'] = '-'
        if 'linewidth' not in grid:
            grid['linewidth'] = .1

        ax.plot(ext_support[1], ext_probabilities[0], **right_points)
        if self.complete_left:
            ax.hlines(y=ext_probabilities[0], xmin=ext_support[0], xmax=ext_support[1], **left_line_complete)
        else:
            ax.hlines(y=ext_probabilities[0], xmin=ext_support[0], xmax=ext_support[1], **left_line_incomplete)
        if self.complete_right:
            ax.hlines(y=1, xmin=ext_support[ext_support.size - 2], xmax=ext_support[ext_support.size - 1],
                      **right_line_complete)
        else:
            ax.hlines(y=ext_probabilities[-1], xmin=ext_support[ext_support.size - 2],
                      xmax=ext_support[ext_support.size - 1], **right_line_incomplete)
        for x in range(1, ext_support.size - 2):
            ax.plot(ext_support[x], ext_probabilities[x], **left_points)
            ax.plot(ext_support[x + 1], ext_probabilities[x], **right_points)
            ax.hlines(y=ext_probabilities[x], xmin=ext_support[x], xmax=ext_support[x + 1], **hlines)
        plt.plot(ext_support[ext_support.size - 2], ext_probabilities[ext_support.size - 2], **left_points)
        plt.title('Cumulative Distribution Function for ' + rv_name.upper())
        #plt.axis('off')
        plt.xlabel(rv_name.lower())
        plt.ylabel(f'F({rv_name.lower()})')

        if x_y_ticks and len(self.__support) <= x_y_ticks:
            ax.set_xticks(self.__support)
            ax.set_yticks(self.__cum_prob)
        if grid:
            plt.grid(b=True, **grid)
        

        if save:
            file_name = graph_name + '_cdf_' + rv_name + '.png'
            plt.savefig(file_name, format='png', dpi=600)

        plt.show()
        return fig, ax

    def plot_pmf(self, rv_name='X', graph_name='', points=dict(),
                 left_line_incomplete=dict(), right_line_incomplete=dict(),
                 grid=dict(), x_y_ticks=10, save=True):
        '''
        The method used to plot the probability mass function.

        :param rv_name: The name that will appear in the title.
        :param graph_name: the graph's name used to save the file
        :param points: A dictionary so you can pass whatever parameters to the points in the plots.
        :param left_line_incomplete: A dictionary so you can pass whatever parameters to the left (the first) line in the case the left tail is incomplete.
        :param right_line_incomplete: A dictionary so you can pass whatever parameters to the right line (the last) in the case the left tail is incomplete.
        :param grid: A dictionary so you can pass whatever parameters to the grid's design.
        :param x_y_ticks: The number of axis x and axis y thicks that you want to use. If the number passed is below the supports's cardinality the default will be used. This is necessary or you'll end up with a graph to much populated in the axis and difficult to read.
        :param save: If you want to save the graph plotted. By default will save an png file, but you can always change it by calling the figure returned (see returns below).

        :return: A tuple with the figure and the plot.
        '''

        fig, ax = plt.subplots()
        if 'color' not in points:
            points['color'] = 'black'
        if 'marker' not in points:
            points['marker'] = 'o'
        if 'linestyle' not in points:
            points['linestyle'] = '--'

        if 'linestyle' not in left_line_incomplete:
            left_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in left_line_incomplete:
            left_line_incomplete['linewidth'] = 2
        if 'color' not in left_line_incomplete:
            left_line_incomplete['color'] = 'r'

        if 'linestyle' not in right_line_incomplete:
            right_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in right_line_incomplete:
            right_line_incomplete['linewidth'] = 2
        if 'color' not in right_line_incomplete:
            right_line_incomplete['color'] = 'r'

        if grid is not None:
            if 'which' not in grid:
                grid['which'] = 'both'
            if 'axis' not in grid:
                grid['axis'] = 'both'
            if 'color' not in grid:
                grid['color'] = 'grey'
            if 'linestyle' not in grid:
                grid['linestyle'] = '-'
            if 'linewidth' not in grid:
                grid['linewidth'] = .1

        # plt.bar(self.__support, self.__prob, width=.1, color='k')
        plt.plot(self.support, self.__prob, **points)  # 'ko--'
        plt.title('Probability Mass Function for ' + rv_name.upper())
        plt.xlabel(rv_name.lower())
        plt.ylabel(f'f({rv_name.lower()})')
        if x_y_ticks and len(self.__support) <= x_y_ticks:
            ax.set_xticks(self.__support)
            ax.set_yticks(self.__prob)
        if not self.__complete_left:
            increment = np.average(np.diff(self.__support))
            ax.hlines(y=self.__prob[0], xmin=self.__support[0] - increment,
                      xmax=self.__support[0], **left_line_incomplete)
        if not self.__complete_right:
            increment = np.average(np.diff(self.__support))
            ax.hlines(y=self.__prob[-1], xmin=self.__support[len(self.__support) - 1],
                      xmax=self.__support[len(self.__support) - 1] + increment,
                      **right_line_incomplete)
        if grid and grid is not None:
            plt.grid(b=True, **grid)



        if save:
            file_name = graph_name + '_pmf_' + rv_name + '.png'
            plt.savefig(file_name, format='png', dpi=600)

        plt.show()
        return fig, ax

    def plot_quantile(self, rv_name='X', graph_name='', left_points=dict(), right_points=dict(), hlines=dict(),
                      left_line_complete=dict(), right_line_complete=dict(),
                      left_line_incomplete=dict(), right_line_incomplete=dict(),
                      grid=dict(), x_y_ticks=10, save=True):
        '''
        The method used to plot the percentile (quantile) function.

        :param rv_name: The name that will appear in the title.
        :param graph_name: the graph's name used to save the file
        :param left_points: A dictionary so you can pass whatever parameters to the left points in the plots.
        :param right_points: A dictionary so you can pass whatever parameters to the right points in the plots.
        :param hlines: A dictionary so you can pass whatever parameters to horizontal lines in the plots.
        :param left_line_complete: A dictionary so you can pass whatever parameters to the left (the first) line in the case the left tail is complete.
        :param right_line_complete: A dictionary so you can pass whatever parameters to the right line (the last) in the case the left tail is complete.
        :param left_line_incomplete: A dictionary so you can pass whatever parameters to the left (the first) line in the case the left tail is incomplete.
        :param right_line_incomplete: A dictionary so you can pass whatever parameters to the right line (the last) in the case the left tail is incomplete.
        :param grid: A dictionary so you can pass whatever parameters to the grid's design.
        :param x_y_ticks: The number of axis x and axis y thicks that you want to use. If the number passed is below the supports's cardinality the default will be used. This is necessary or you'll end up with a graph to much populated in the axis and difficult to read.
        :param save: If you want to save the graph plotted. By default will save an png file, but you can always change it by calling the figure returned (see returns below).

        :return: A tuple with the figure and the plot.
        '''
        increment = np.average(np.diff(self.__cum_prob))
        # ext_probabilities = np.append(self.__cum_prob, self.__cum_prob[-1] + increment)
        ext_probabilities = np.insert(self.__cum_prob, 0, self.__cum_prob[0] - increment)
        ext_support = np.insert(self.__support, 0, self.__support[0])

        fig, ax = plt.subplots()
        if 'markerfacecolor' not in left_points:
            left_points['markerfacecolor'] = 'white'
        if 'markeredgecolor' not in left_points:
            left_points['markeredgecolor'] = 'black'
        if 'marker' not in left_points:
            left_points['marker'] = 'o'

        if 'markerfacecolor' not in right_points:
            right_points['markerfacecolor'] = 'black'
        if 'markeredgecolor' not in right_points:
            right_points['markeredgecolor'] = 'black'
        if 'marker' not in right_points:
            right_points['marker'] = 'o'

        if 'linestyle' not in left_line_complete:
            left_line_complete['linestyle'] = 'dashed'
        if 'linewidth' not in left_line_complete:
            left_line_complete['linewidth'] = 2
        if 'color' not in left_line_complete:
            left_line_complete['color'] = 'k'

        if 'linestyle' not in right_line_complete:
            right_line_complete['linestyle'] = 'dashed'
        if 'linewidth' not in right_line_complete:
            right_line_complete['linewidth'] = 2
        if 'color' not in right_line_complete:
            right_line_complete['color'] = 'k'

        if 'linestyle' not in left_line_incomplete:
            left_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in left_line_incomplete:
            left_line_incomplete['linewidth'] = 2
        if 'color' not in left_line_incomplete:
            left_line_incomplete['color'] = 'r'

        if 'linestyle' not in right_line_incomplete:
            right_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in right_line_incomplete:
            right_line_incomplete['linewidth'] = 2
        if 'color' not in right_line_incomplete:
            right_line_incomplete['color'] = 'r'

        if 'linewidth' not in hlines:
            hlines['linewidth'] = 2
        if 'color' not in hlines:
            hlines['color'] = 'k'

        if 'which' not in grid:
            grid['which'] = 'both'
        if 'axis' not in grid:
            grid['axis'] = 'both'
        if 'color' not in grid:
            grid['color'] = 'grey'
        if 'linestyle' not in grid:
            grid['linestyle'] = '-'
        if 'linewidth' not in grid:
            grid['linewidth'] = .1

        ax.plot(ext_probabilities[1], ext_support[0], **right_points)
        if self.complete_left:
            ax.hlines(y=ext_support[0], xmin=ext_probabilities[0], xmax=ext_probabilities[1], **left_line_complete)
        else:
            ax.hlines(y=ext_support[0], xmin=ext_probabilities[0], xmax=ext_probabilities[1], **left_line_incomplete)
        if self.complete_right:
            ax.hlines(y=ext_support[-1], xmin=ext_probabilities[ext_probabilities.size - 2],
                      xmax=ext_probabilities[ext_probabilities.size - 1] + increment, **right_line_complete)
        else:
            ax.hlines(y=ext_support[-1], xmin=ext_probabilities[ext_probabilities.size - 2],
                      xmax=ext_probabilities[ext_probabilities.size - 1] + increment, **right_line_incomplete)
        for x in range(1, ext_probabilities.size - 2):
            ax.plot(ext_probabilities[x], ext_support[x + 1], **left_points)
            ax.plot(ext_probabilities[x + 1], ext_support[x + 1], **right_points)
            ax.hlines(y=ext_support[x + 1], xmin=ext_probabilities[x], xmax=ext_probabilities[x + 1], **hlines)
        plt.plot(ext_probabilities[ext_probabilities.size - 2], ext_support[ext_probabilities.size - 1], **left_points)
        plt.title('Quantile Function for ' + rv_name.upper())
        plt.xlabel('p')
        plt.ylabel('$F\overleftarrow{(p)}$')

        if x_y_ticks and len(self.__support) <= x_y_ticks:
            ax.set_xticks(self.__cum_prob)
            ax.set_yticks(self.__support)
        if grid:
            plt.grid(b=True, **grid)
        

        if save:
            file_name = graph_name + '_quantile_' + rv_name + '.png'
            plt.savefig(file_name, format='png', dpi=600)

        plt.show()
        return fig, ax

    def plot_sf(self, rv_name='X', graph_name='', left_points=dict(), right_points=dict(), hlines=dict(),
                 left_line_complete=dict(), right_line_complete=dict(),
                 left_line_incomplete=dict(), right_line_incomplete=dict(),
                 grid=dict(), x_y_ticks=10, save=True):
        '''
        The method used to plot the cumulative distribution function.

        :param rv_name: The name that will appear in the title.
        :param graph_name: the graph's name used to save the file
        :param left_points: A dictionary so you can pass whatever parameters to the left points in the plots.
        :param right_points: A dictionary so you can pass whatever parameters to the right points in the plots.
        :param hlines: A dictionary so you can pass whatever parameters to horizontal lines in the plots.
        :param left_line_complete: A dictionary so you can pass whatever parameters to the left (the first) line in the case the left tail is complete.
        :param right_line_complete: A dictionary so you can pass whatever parameters to the right line (the last) in the case the left tail is complete.
        :param left_line_incomplete: A dictionary so you can pass whatever parameters to the left (the first) line in the case the left tail is incomplete.
        :param right_line_incomplete: A dictionary so you can pass whatever parameters to the right line (the last) in the case the left tail is incomplete.
        :param grid: A dictionary so you can pass whatever parameters to the grid's design.
        :param x_y_ticks: The number of axis x and axis y thicks that you want to use. If the number passed is below the supports's cardinality the default will be used. This is necessary or you'll end up with a graph to much populated in the axis and difficult to read.
        :param save: If you want to save the graph plotted. By default will save an png file, but you can always change it by calling the figure returned (see :return below).

        :return: A tuple with the figure and the plot.
        '''
        increment = np.average(np.diff(self.__support))
        ext_support = np.append(self.__support, self.__support[-1] + increment)
        ext_support = np.insert(ext_support, 0, self.__support[0] - increment)
        ext_probabilities = 1-np.insert(self.__cum_prob, 0, 0)

        fig, ax = plt.subplots()
        if 'markerfacecolor' not in left_points:
            left_points['markerfacecolor'] = 'black'
        if 'markeredgecolor' not in left_points:
            left_points['markeredgecolor'] = 'black'
        if 'marker' not in left_points:
            left_points['marker'] = 'o'

        if 'markerfacecolor' not in right_points:
            right_points['markerfacecolor'] = 'white'
        if 'markeredgecolor' not in right_points:
            right_points['markeredgecolor'] = 'black'
        if 'marker' not in right_points:
            right_points['marker'] = 'o'

        if 'linestyle' not in left_line_complete:
            left_line_complete['linestyle'] = 'dashed'
        if 'linewidth' not in left_line_complete:
            left_line_complete['linewidth'] = 2
        if 'color' not in left_line_complete:
            left_line_complete['color'] = 'k'

        if 'linestyle' not in right_line_complete:
            right_line_complete['linestyle'] = 'dashed'
        if 'linewidth' not in right_line_complete:
            right_line_complete['linewidth'] = 2
        if 'color' not in right_line_complete:
            right_line_complete['color'] = 'k'

        if 'linestyle' not in left_line_incomplete:
            left_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in left_line_incomplete:
            left_line_incomplete['linewidth'] = 2
        if 'color' not in left_line_incomplete:
            left_line_incomplete['color'] = 'r'

        if 'linestyle' not in right_line_incomplete:
            right_line_incomplete['linestyle'] = ':'
        if 'linewidth' not in right_line_incomplete:
            right_line_incomplete['linewidth'] = 2
        if 'color' not in right_line_incomplete:
            right_line_incomplete['color'] = 'r'

        if 'linewidth' not in hlines:
            hlines['linewidth'] = 2
        if 'color' not in hlines:
            hlines['color'] = 'k'

        if 'which' not in grid:
            grid['which'] = 'both'
        if 'axis' not in grid:
            grid['axis'] = 'both'
        if 'color' not in grid:
            grid['color'] = 'grey'
        if 'linestyle' not in grid:
            grid['linestyle'] = '-'
        if 'linewidth' not in grid:
            grid['linewidth'] = .1

        ax.plot(ext_support[1], ext_probabilities[0], **right_points)
        if self.complete_left:
            ax.hlines(y=ext_probabilities[0], xmin=ext_support[0], xmax=ext_support[1], **left_line_complete)
        else:
            ax.hlines(y=ext_probabilities[0], xmin=ext_support[0], xmax=ext_support[1], **left_line_incomplete)
        if self.complete_right:
            ax.hlines(y=0, xmin=ext_support[ext_support.size - 2], xmax=ext_support[ext_support.size - 1],
                      **right_line_complete)
        else:
            ax.hlines(y=ext_probabilities[-1], xmin=ext_support[ext_support.size - 2],
                      xmax=ext_support[ext_support.size - 1], **right_line_incomplete)
        for x in range(1, ext_support.size - 2):
            ax.plot(ext_support[x], ext_probabilities[x], **left_points)
            ax.plot(ext_support[x + 1], ext_probabilities[x], **right_points)
            ax.hlines(y=ext_probabilities[x], xmin=ext_support[x], xmax=ext_support[x + 1], **hlines)
        plt.plot(ext_support[ext_support.size - 2], ext_probabilities[ext_support.size - 2], **left_points)
        plt.title('Survival Distribution Function for ' + rv_name.upper())
        plt.xlabel(rv_name.lower())
        plt.ylabel(f'S({rv_name.lower()})')

        if x_y_ticks and len(self.__support) <= x_y_ticks:
            ax.set_xticks(self.__support)
            ax.set_yticks(1-self.__cum_prob)
        if grid:
            plt.grid(b=True, **grid)

        if save:
            file_name = graph_name + '_cdf_' + rv_name + '.png'
            plt.savefig(file_name, format='png', dpi=600)

        plt.show()
        return fig, ax