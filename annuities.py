__author__ = "PedroCR"

import numpy as np
import mortality_table as mt


# life annuities
def axy(mtx, mty, x, y, i=None, g=0, m=1):
    '''
    computes a whole life annuity immediate paying while both lives are alive
    :param mtx: table for life x
    :param mty: table for life y
    :param x: age x
    :param y: age y
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :return: the actuarial present value
    '''
    years_to_wx = mtx.w - x
    years_to_wy = mty.w - y
    years_to_end = np.max(np.min((years_to_wx, years_to_wy)), 0)
    i = i / 100
    g = g / 100
    d = float((1 + g) / (1 + i))
    instalments = [mtx.tpx(x, t=t) * mty.tpx(y, t=t) * np.power(d, t) for t in range(1, years_to_end + 1)]
    instalments = np.array(instalments) / (1 + g)

    return np.sum(instalments)
