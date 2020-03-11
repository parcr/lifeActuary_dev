__author__ = "PedroCR"

import numpy as np


# todo test this module
# life generic annuity 2 head
def annuity_xy(mtx, mty, x, x_first, x_last, y, i=None, g=.0, m=1, method='udd'):
    '''
    Computes the present value of an annuity that starts paying 1 at age x, increasing by (1+g/100) and stops
    at age x_w, paying (1+g)^{t-1}
    :param mtx: table for life x
    :param mty: table for life y
    :param x: age x
    :param y: age y
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
    if y < 0: return np.nan
    i = i / 100
    g = g / 100
    d = float((1 + g) / (1 + i))
    number_of_payments = int((x_last - x_first) * m + 1)
    payments_instants = np.linspace(x_first - x, x_last - x, number_of_payments)
    instalments = [mtx.tpx(x, t=t, method=method) * mty.tpx(y, t=t, method=method) *
                   np.power(d, t)
                   for t in payments_instants]
    instalments = np.array(instalments) / np.power(1 + g, x_first - x) / m
    return np.sum(instalments)


# life annuities 2 head
# immediate
def axy(mtx, mty, x, y, i=None, g=0, m=1, method='udd'):
    '''
    Returns a whole life annuity immediate
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
    if x + 1 / m > mtx.w: return 0

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first=x + 1 / m, x_last=mtx.w, y=y, i=i, g=g, m=m, method=method)


def t_axy(mtx, mty, x, y, i=None, g=0, m=1, defer=0, method='udd'):
    '''
    Returns a whole life annuity immediate, deferred
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
    if x + 1 / m + defer > mtx.w: return 0

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first=x + 1 / m + defer, x_last=mtx.w, y=y, i=i, g=g, m=m, method=method)


def naxy(mtx, mty, x, y, n, i=None, g=0, m=1, method='udd'):
    '''
    Return the actuarial present value of a (immediate) temporal (term certain) annuity: n-year temporary
    life annuity-late. Payable 'm' per year at the ends of the period
    :param mtx: table for life x
    :param mty: table for life y
    :param x: age x
    :param y: age y
    :param n: total amount payed
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''
    if x + 1 / m > mtx.w: return 0

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first=x + 1 / m, x_last=x + n, y=y, i=i, g=g, m=m, method=method)


def t_naxy(mtx, mty, x, y, n, i=None, g=0, m=1, defer=0, method='udd'):
    '''
    Return the actuarial present value of a (immediate) temporal (term certain) annuity: n-year temporary
    life annuity-late. Payable 'm' per year at the ends of the period, deferred
    :param mtx: table for life x
    :param mty: table for life y
    :param x: age x
    :param y: age y
    :param n: total amount payed
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''
    if x + 1 / m + defer > mtx.w: return 0

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first=x + 1 / m + defer, x_last=x + n + defer, y=y,
                      i=i, g=g, m=m, method=method)


# due
def aaxy(mtx, mty, x, y, i=None, g=0, m=1, method='udd'):
    '''
    Returns a whole life annuity due
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
    if x > mtx.w: return 1

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first=x, x_last=mtx.w, y=y, i=i, g=g, m=m, method=method)


def t_aaxy(mtx, mty, x, y, i=None, g=0, m=1, defer=0, method='udd'):
    '''
    Returns a whole life annuity due, deferred
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
    if x + defer > mtx.w: return 0

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first=x + defer, x_last=mtx.w, y=y, i=i, g=g, m=m, method=method)


def naaxy(mtx, mty, x, y, n, i=None, g=0, m=1, method='udd'):
    '''
    Return the actuarial present value of a (due) temporal (term certain) annuity: n-year temporary
    life annuity-due. Payable 'm' per year at the ends of the period
    :param mtx: table for life x
    :param mty: table for life y
    :param x: age x
    :param y: age y
    :param n: total amount payed
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''
    if x > mtx.w: return 1

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first=x, x_last=x + n - 1 / m, y=y, i=i, g=g, m=m, method=method)


def t_naaxy(mtx, mty, x, y, n, i=None, g=0, m=1, defer=0, method='udd'):
    '''
    Return the actuarial present value of a (due) temporal (term certain) annuity: n-year temporary
    life annuity-due. Payable 'm' per year at the ends of the period, deferred
    :param mtx: table for life x
    :param mty: table for life y
    :param x: age x
    :param y: age y
    :param n: total amount payed
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param m: frequency of payments per unit of interest rate quoted
    :param defer: deferment period
    :param method: the method to approximate the fractional periods
    :return: the actuarial present value
    '''
    if x + defer > mtx.w: return 0

    return annuity_xy(mtx=mtx, mty=mty, x=x, x_first=x + defer, x_last=x + n + defer - 1 / m, y=y,
                      i=i, g=g, m=m, method=method)


def nExy(mtx, mty, x, y, i=None, g=0, defer=0, method='udd'):
    """
    Pure endowment or Deferred capital
    :param x: x age at the beginning of the contract
    :param y: y age at the beginning of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param defer: deferment period
    :param method: the method to approximate the fractional periods
    :return: the present value of a pure endowment of 1 at age x+n
    """

    return t_naaxy(mtx, mty, x, y, n=1, i=i, g=g, m=1, defer=defer, method=method)
