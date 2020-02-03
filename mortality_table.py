__author__ = "PedroCR"

import numpy as np
import pandas as pd


class MortalityTable:
    '''
    Instantiates a life table, where you can pass it in the form of the lx, qx or px. Note that the first value is
    the first age considered in the table.
    The life table will be complete, that is, from age 0 to age w, that is, the last age where lx>0.
    '''

    def __init__(self, data_type='q', mt=None, perc=100):
        if data_type not in ('l', 'q', 'p'):
            return
        if not mt:
            return
        self.__methods = ('udd', 'cfm', 'bal')
        self.mt = mt
        self.x0 = mt[0]
        self.w = 0
        self.lx = []
        self.px = []
        self.qx = []
        self.dx = []
        self.ex = []
        self.perc = perc
        self.msn = []

        radical = 100000.
        pperc = perc / 100.
        mt = np.array(mt[1:])
        if data_type == 'l':
            if mt[-1] > 0:
                mt = np.append(mt, 0)
            self.qx = (mt[:-1] - mt[1:]) / mt[:-1] * pperc
            # self.qx = np.append(np.zeros(self.x0), self.qx)
        if data_type == 'q':
            self.qx = mt * pperc
        if data_type == 'p':
            self.qx = (1 - mt) * pperc

        if self.qx[-1] < 1 - .1e-10:
            self.qx = np.append(self.qx, 1)
        self.qx = np.append(np.zeros(self.x0), self.qx)

        self.px = 1 - self.qx
        self.lx = np.array([radical] * (len(self.qx) + 1))
        self.dx = np.array([-1] * len(self.qx))
        self.ex = np.array([-1] * len(self.qx))
        for idx_p, p in enumerate(self.px):
            self.lx[idx_p + 1] = self.lx[idx_p] * p
        self.dx = self.lx[:-1] * self.qx
        sum_lx = np.array([sum(self.lx[l:]) for l in range(len(self.qx))])
        self.ex = sum_lx[1:] / self.lx[:-2]
        self.ex = np.append(self.ex, 0) + .5
        self.w = len(self.lx) - 2

    def df_life_table(self):
        data = {'x': np.arange(self.w + 1), 'lx': self.lx[:-1], 'dx': self.dx,
                'qx': self.qx, 'px': self.px, 'exo': self.ex}
        df = pd.DataFrame(data)
        df = df.astype({'x': 'int8'})
        return df

    def lx_udd(self, t):
        if t > self.w:
            return 0.
        if t < 0:
            return np.nan
        int_t = np.int(t)
        frac_t = t - int_t
        if frac_t == 0:
            return self.lx[int_t]
        else:
            return self.lx[int_t] * (1 - frac_t) + self.lx[int_t + 1] * frac_t

    def lx_cfm(self, t):
        if t > self.w:
            return 0.
        if t < 0:
            return np.nan
        int_t = np.int(t)
        frac_t = t - int_t
        if frac_t == 0:
            return self.lx[int_t]
        else:
            return self.lx[int_t] * np.power(self.lx[int_t + 1] / self.lx[int_t], frac_t)

    def lx_bal(self, t):
        if t > self.w:
            return 0.
        if t < 0:
            return np.nan
        int_t = np.int(t)
        frac_t = t - int_t
        if frac_t == 0:
            return self.lx[int_t]
        else:
            inv_lx = 1 / self.lx[int_t] - frac_t * (1 / self.lx[int_t] - 1 / self.lx[int_t + 1])
            return 1 / inv_lx

    def get_lx_method(self, x, method='udd'):
        if method not in self.__methods:
            return np.nan
        if x < 0:
            return np.nan
        if x > self.w:
            return 0
        if method == 'udd':
            return self.lx_udd(x)
        elif method == 'cfm':
            return self.lx_cfm(x)
        elif method == 'bal':
            return self.lx_bal(x)
        else:
            return np.nan

    def tqx(self, x, t=1, method='udd'):
        '''
        Obtains the probability that a life x dies before x+t
        :param method: the method used to approximate lx for non-integer x's
        :param x: age at beginning
        :param t: period
        :return: probability of x dying before x+t
        '''
        if method not in self.__methods:
            return np.nan
        if x < 0:
            return np.nan
        if t <= 0:
            return .0
        if x + t > self.w:
            return 1.
        l_x = self.get_lx_method(x, method)
        l_x_t = self.get_lx_method(x + t, method)
        self.msn.append(f"{t}_q_{x}=1-({l_x_t} / {l_x})")
        return 1 - l_x_t / l_x

    def tpx(self, x, t=1, method='udd'):
        '''
        Obtains the probability that a life x dies before x+t
        :param method: the method used to approximate lx for non-integer x's
        :param x: age at beginning
        :param t: period
        :return: probability of x dying before x+t
        '''
        if method not in self.__methods:
            return np.nan
        if x < 0:
            return np.nan
        if t <= 0:
            return 1.
        if x + t > self.w:
            return 0.
        l_x = self.get_lx_method(x, method)
        l_x_t = self.get_lx_method(x + t, method)
        self.msn.append(f"{t}_p_{x}={l_x_t} / {l_x}")
        return l_x_t / l_x

    def t_nqx(self, x, t=1, n=1, method='udd'):
        '''
        Obtains the probability that a life x dies survives to age x+t and dies before x+t+n
        :param method: the method used to approximate lx for non-integer x's
        :param x: age at beginning
        :param t: period
        :return: probability of x dying before x+t
        '''
        l_x = self.get_lx_method(x, method)
        l_x_t = self.get_lx_method(x + t, method)
        l_x_t_n = self.get_lx_method(x + t + n, method)
        self.msn.append(f"{t}|{n}_q_{x}={t}_p_{x}  {n}_q_{x + t}={l_x_t} / {l_x} ({l_x_t}-{l_x_t_n}) / {l_x_t}")
        return (l_x_t - l_x_t_n) / l_x
