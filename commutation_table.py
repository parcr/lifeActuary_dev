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
        self.v = 1 / (1 + self.i)
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
        df = pd.concat([data_lf, df], axis=1, sort=False)  # todo
        return df

    def nEx(self, x, n):
        """
        Pure endowment or Deferred capital
        :param x: age at the beginning of the contract
        :param n: years until payment, if x is alive
        :return: the present value of a pure endowment of 1 at age x+n
        """
        if x < 0:
            return np.nan
        if n <= 0:
            return 1
        if x + n > self.w:
            return 0.
        D_x = self.Dx[x]
        D_x_n = self.Dx[x + n]
        self.msn.append(f"{n}_E_{x}={D_x_n} / {D_x}")
        return D_x_n / D_x

    def Ax(self, x):
        """
        Whole life insurance
        :param x: age at the beginning of the contract
        :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1,at the
        end of the year of death. It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
        """
        if x < 0:
            return np.nan
        if x > self.w:
            return self.v
        D_x = self.Dx[x]
        M_x = self.Mx[x]
        self.msn.append(f"A_{x}={M_x} / {D_x}")
        return M_x / D_x
