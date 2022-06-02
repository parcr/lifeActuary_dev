__author__ = "PedroCR"

import numpy as np


# life generic annuity 1 head
def annuity_x(mt, x, x_first, x_last, i=None, g=.0, m=1, method='udd'):
    '''
    Computes the present value of an annuity that starts paying 1 ate age x, increasing by (1+g/100) and stops
    at age x_t_w, paying (1+g)^{t-1}
    :param mt: table for life x
    :param x: age x
    :param x_first: age of first payment
    :param x_last: age of final payment
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''
    if x_first < x: return np.nan
    if x_last < x_first == x: return np.nan
    if int(m) != m: return np.nan
    if x == x_first == x_last: return 1
    i = i / 100
    g = g / 100
    d = float((1 + g) / (1 + i))
    number_of_payments = int((x_last - x_first) * m + 1)
    payments_instants = np.linspace(x_first - x, x_last - x, number_of_payments)
    instalments = [mt.npx(x, n=t, method=method) *
                   np.power(d, t) for t in payments_instants]
    instalments = np.array(instalments) / np.power(1 + g, x_first - x) / m
    return np.sum(instalments)


# life annuities_1 1 head
def ax(mtx, x, i=None, g=0, m=1, defer=0, method='udd'):
    '''
    computes a whole life annuity immediate paying while both lives are alive
    :param mtx: table for life x
    :param x: age x
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''
    years_to_wx = mtx.w - (x + defer) + 1
    years_to_end = np.max(years_to_wx, 0)
    i = i / 100
    g = g / 100
    d = float((1 + g) / (1 + i))
    if years_to_end == 0:  # at least one will die before the end of the period
        return .0
    number_of_payments = int(years_to_end * m - 1)
    # starts paying one period after the deferment
    payments_instants = np.linspace(defer + 1 / m, years_to_end - 1, number_of_payments)
    instalments = [mtx.npx(x, n=t, method=method) *
                   np.power(d, t) for t in payments_instants]
    instalments = np.array(instalments) / np.power(1 + g, defer) / m

    return np.sum(instalments)


def aax(mtx, x, i=None, g=0, m=1, defer=0, method='udd'):
    '''
    computes a whole life annuity due paying while both lives are alive
    :param mtx: table for life x
    :param x: age x
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''

    years_to_wx = mtx.w - (x + defer) + 1
    years_to_end = np.max(years_to_wx, 0)
    i = i / 100
    g = g / 100
    d = float((1 + g) / (1 + i))
    if years_to_end == 0:  # at least one will die before the end of the period
        return .0
    number_of_payments = int(years_to_end * m)
    # starts paying immediately after the deferment
    payments_instants = np.linspace(defer + 1 / m * 0, years_to_end, number_of_payments)
    instalments = [mtx.npx(x, n=t, method=method) *
                   np.power(d, t) for t in payments_instants]
    instalments = np.array(instalments) / np.power(1 + g, defer) / m

    return np.sum(instalments)


# life annuities_1 2 heads
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
    years_to_wx = mtx.w - (x + defer) + 1
    years_to_wy = mty.w - (y + defer) + 1
    years_to_end = np.max(np.min((years_to_wx, years_to_wy)), 0)
    i = i / 100
    g = g / 100
    d = float((1 + g) / (1 + i))
    if years_to_end == 0:  # at least one will die before the end of the period
        return .0
    number_of_payments = int(years_to_end * m - 1)
    # starts paying one period after the deferment
    payments_instants = np.linspace(defer + 1 / m, years_to_end - 1, number_of_payments)
    instalments = [mtx.npx(x, n=t, method=method) * mty.npx(y, n=t, method=method) *
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

    years_to_wx = mtx.w - (x + defer) + 1
    years_to_wy = mty.w - (y + defer) + 1
    years_to_end = np.max(np.min((years_to_wx, years_to_wy)), 0)
    i = i / 100
    g = g / 100
    d = float((1 + g) / (1 + i))
    if years_to_end == 0:  # at least one will die before the end of the period
        return .0
    number_of_payments = int(years_to_end * m)
    # starts paying immediately after the deferment
    payments_instants = np.linspace(defer + 1 / m * 0, years_to_end, number_of_payments)
    instalments = [mtx.npx(x, n=t, method=method) * mty.npx(y, n=t, method=method) *
                   np.power(d, t) for t in payments_instants]
    instalments = np.array(instalments) / np.power(1 + g, defer) / m

    return np.sum(instalments)
