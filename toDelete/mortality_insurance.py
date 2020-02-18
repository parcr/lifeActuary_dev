__author__ = "PedroCR"

import numpy as np


def A_x(mt, x, x_first, x_last, i=None, g=.0, method='udd'):
    """
    Whole life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param x_first: age of first payment
    :param x_last: age of final payment
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1,at the
    end of the year of death. It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """
    if x_first < x: return np.nan
    if x_last < x_first == x: return np.nan
    if x == x_first == x_last: return 1
    i = i / 100
    g = g / 100
    d = float((1 + g) / (1 + i))
    number_of_payments = int((x_last - x_first) + 1)
    payments_instants = np.linspace(x_first - x, x_last - x, number_of_payments)
    instalments = [mt.tpx(x, t=t, method=method) * mt.tqx(x + t, t=1, method=method) * np.power(d, t)
                   for t in payments_instants]
    instalments = np.array(instalments) / np.power(1 + g, x_first - x) / m
    return np.sum(instalments)
