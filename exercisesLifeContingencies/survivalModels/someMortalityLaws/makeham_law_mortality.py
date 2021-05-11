import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import scipy.integrate


def mu(a, b, c, x):
    if x < 0 or a < 0 or (b <= 0 or b >= 1) or c <= 1:
        return np.nan
    return a + b * np.power(c, x)


def S(a, b, c, x, t):
    if x < 0 or a < 0 or (b <= 0 or b >= 1) or c <= 1:
        return np.nan
    if t < 0:
        return 1
    else:
        return np.exp(-b / np.log(c) * np.power(c, x) * (np.power(c, t) - 1)) * np.exp(-a * t)


