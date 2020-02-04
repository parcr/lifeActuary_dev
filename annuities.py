__author__ = "PedroCR"

import numpy as np


# life annuities
def axy(mtx, mty, x, y, i=None, g=0, m=1, defer=0, method='udd'):
    '''
    computes a whole life annuity immediate paying while both lives are alive
    :param mtx: table for life x
    :param mty: table for life y
    :param x: age x
    :param y: age y
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''
    years_to_wx = mtx.w - (x + defer)
    years_to_wy = mty.w - (y + defer)
    years_to_end = np.max(np.min((years_to_wx, years_to_wy)), 0)
    i = i / 100
    g = g / 100
    d = float((1 + g) / (1 + i))
    if years_to_end == 0:  # at least one will die before the end of the period
        return .0
    number_of_payments = int(years_to_end * m)
    payments_instants = np.linspace(defer + 1 / m, years_to_end, number_of_payments)
    instalments = [mtx.tpx(x, t=t, method=method) * mty.tpx(y, t=t, method=method) *
                   np.power(d, t) for t in payments_instants]
    instalments = np.array(instalments) / np.power(1 + g, defer) / m

    return np.sum(instalments)


def aaxy(mtx, mty, x, y, i=None, g=0, m=1, defer=0, method='udd'):
    '''
    computes a whole life annuity due paying while both lives are alive
    :param mtx: table for life x
    :param mty: table for life y
    :param x: age x
    :param y: age y
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''

    return 1 / m / np.power(1 + g, defer) + axy(mtx, mty, x, y, i, g, m, defer, method)
