import numpy as np
import scipy.integrate
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]


class Makeham:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def mu(self, x):
        if x < 0 or self.a < 0 or (self.b <= 0 or self.b >= 1) or self.c <= 1:
            return np.nan
        return self.a + self.b * np.power(self.c, x)

    def S(self, x, t):
        if x < 0 or self.a < 0 or (self.b <= 0 or self.b >= 1) or self.c <= 1:
            return np.nan
        if t < 0:
            return 1
        else:
            return np.exp(-self.b / np.log(self.c) * np.power(self.c, x) *
                          (np.power(self.c, t) - 1)) * np.exp(-self.a * t)

    def pdf(self, x, t):
        if x < 0 or self.a < 0 or (self.b <= 0 or self.b >= 1) or self.c <= 1:
            return np.nan
        if t < 0:
            return 1
        else:
            return (self.a + self.b * np.power(self.c, x + t)) * \
                   np.exp(-self.b / np.log(self.c) * np.power(self.c, x) *
                          (np.power(self.c, t) - 1)) * np.exp(-self.a * t)

    def moments_Tx(self, x=0, k=1):
        if x < 0 or k < 0:
            return np.nan
        if k == 0:
            return 1

        def t_S_x(t):
            return k * np.power(t, k - 1) * \
                   np.exp(-self.b / np.log(self.c) * np.power(self.c, x) * (np.power(self.c, t) - 1)) * np.exp(
                -self.a * t)

        ev = scipy.integrate.quad(t_S_x, 0, np.inf)
        return ev

    def expected_value_Tx(self, x=0):
        return self.moments_Tx(x=x, k=1)[0]

    def variance_Tx(self, x=0):
        ev = self.expected_value_Tx(x=x)
        ev_square = self.moments_Tx(x=x, k=2)[0]
        return ev_square - np.power(ev, 2)

    def ax(self, x=0, interest_rate=0, n=np.inf):
        if x < 0:
            return np.nan

        def a_x(t, interest_rate=.05):
            v = 1 / (1 + interest_rate)
            return np.power(v, t) * \
                   np.exp(-self.b / np.log(self.c) * np.power(self.c, x) * (np.power(self.c, t) - 1)) * \
                   np.exp(-self.a * t)

        ev = scipy.integrate.quad(a_x, 0, n)
        return ev
