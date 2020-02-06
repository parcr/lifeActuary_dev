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
    instalments = [mt.tpx(x, t=t, method=method) *
                   np.power(d, t) for t in payments_instants]
    instalments = np.array(instalments) / np.power(1 + g, x_first - x) / m
    return np.sum(instalments)


# life annuities 1 head
# immediate
def ax(mt, x, i=None, g=0, m=1, method='udd'):
    '''
    computes a whole life annuity immediate
    :param mt: table for life x
    :param x: age x
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''

    return annuity_x(mt=mt, x=x, x_first=x + 1 / m, x_last=mt.w, i=i, g=g, m=m, method=method)


def t_ax(mt, x, i=None, g=0, m=1, defer=0, method='udd'):
    '''
    computes a whole life annuity immediate
    :param mt: table for life x
    :param x: age x
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''

    return annuity_x(mt=mt, x=x, x_first=x + 1 / m + defer, x_last=mt.w, i=i, g=g, m=m, method=method)


def nax(mt, x, n, i=None, g=0, m=1, method='udd'):
    '''
    Return the actuarial present value of a (immediate) temporal (term certain) annuity: n-year temporary
        life annuity-late. Payable 'm' per year at the ends of the period
    :param mt: table for life x
    :param x: age x
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''

    return annuity_x(mt=mt, x=x, x_first=x + 1 / m, x_last=x + n, i=i, g=g, m=m, method=method)


def t_nax(mt, x, n, i=None, g=0, m=1, defer=0, method='udd'):
    '''
    Return the actuarial present value of a (immediate) temporal (term certain) annuity: n-year temporary
        life annuity-late. Payable 'm' per year at the ends of the period
    :param mt: table for life x
    :param x: age x
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''

    return annuity_x(mt=mt, x=x, x_first=x + 1 / m + defer, x_last=x + n + defer, i=i, g=g, m=m, method=method)


# due
def aax(mt, x, i=None, g=0, m=1, method='udd'):
    '''
    computes a whole life annuity due
    :param mt: table for life x
    :param x: age x
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''

    return annuity_x(mt=mt, x=x, x_first=x, x_last=mt.w, i=i, g=g, m=m, method=method)
