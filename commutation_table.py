__author__ = "PedroCR"

import numpy as np
import pandas as pd
from mortality_table import MortalityTable


class CommutationFunctions(MortalityTable):
    '''
    Instantiates a for a specific mortality table and interest rate, all the usual commutation functions.
    '''

    def __init__(self, i=None, g=0, data_type='q', mt=None, perc=100, app_cont=False):
        MortalityTable.__init__(self, data_type, mt, perc)
        if i is None:
            return
        self.i = i / 100.
        self.g = g / 100.
        self.d = (1 + self.g) / (1 + self.i)
        self.app_cont = app_cont
        self.cont = np.sqrt(1 + self.i)

        # self.Dx = np.array([self.lx[x] * np.power(self.d, x) for x in range(len(self.lx))])
        self.Dx = self.lx[:-1] * np.power(self.d, range(len(self.lx[:-1])))
        self.Nx = np.array([np.sum(self.Dx[x:]) for x in range(len(self.lx[:-1]))])
        self.Cx = self.dx * np.power(self.d, range(1, len(self.dx) + 1))
        self.Mx = np.array([np.sum(self.Cx[x:]) for x in range(len(self.Cx))])
        if self.app_cont:
            self.Mx = self.Mx * self.cont

    def df_commutation_table(self):
        data = {'Dx': self.Dx, 'Nx': self.Nx, 'Cx': self.Cx, 'Mx': self.Mx}
        df = pd.DataFrame(data)
        data_lf = self.df_life_table()
        df = pd.concat([data_lf, df], axis=1, sort=False) # todo
        return df

    def nEx(self, x, n):
        if x < 0:
            return np.nan
        if n <= 0:
            return 1
        if x + n > self.w:
            return 0.

        l_x = self.get_lx_method(x, method)
        l_x_t = self.get_lx_method(x + t, method)
        self.msn.append(f"{t}_q_{x}=1-({l_x_t} / {l_x})")
        return 1 - l_x_t / l_x


