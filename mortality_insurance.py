__author__ = "PedroCR"

import numpy as np
import annuities


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
    if x == x_first == x_last: return 0
    i = i / 100
    g = g / 100
    d = float((1 + g) / (1 + i))
    number_of_payments = int((x_last - x_first) + 1)
    payments_instants = np.linspace(x_first - x, x_last - x, number_of_payments)
    instalments = [mt.tpx(x, t=t - 1, method=method) * mt.tqx(x + t - 1, t=1, method=method) * np.power(d, t)
                   for t in payments_instants]
    instalments = np.array(instalments) / np.power(1 + g, payments_instants[0])
    return np.sum(instalments)


def Ax(mt, x, i=None, g=.0, method='udd'):
    """
    Whole life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1,at the
    end of the year of death. It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """
    return A_x(mt=mt, x=x, x_first=x + 1, x_last=mt.w + 1, i=i, g=g, method=method)


def Ax_(mt, x, i=None, g=.0, method='udd'):
    """
    Whole life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1, at the
    moment of death. It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """
    return Ax(mt=mt, x=x, i=i, g=g, method=method) * np.sqrt(1 + i / 100)


def nAx(mt, x, n, i=None, g=.0, method='udd'):
    """
    Term life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a term (temporary) life insurance (i.e. net single premium), that
    pays 1, at the end of the year of death. It is also commonly referred to as the Actuarial Value or
    Actuarial Present Value.
    """
    return A_x(mt=mt, x=x, x_first=x + 1, x_last=x + n, i=i, g=g, method=method)


def nAx_(mt, x, n, i=None, g=.0, method='udd'):
    """
    Term life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a term (temporary) life insurance (i.e. net single premium), that
    pays 1, at the moment of death. It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """
    return nAx(mt=mt, x=x, n=n, i=i, g=g, method=method) * np.sqrt(1 + i / 100)


def nAEx(mt, x, n, i=None, g=.0, method='udd'):
    """
    Endowment insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of an Endowment life insurance (i.e. net single premium), that
    pays 1, at the end of year of death or 1 if x survives to age x+n. It is also commonly referred to as the
    Actuarial Value or Actuarial Present Value.
    """
    return nAx(mt=mt, x=x, n=n, i=i, g=g, method=method) + annuities.nEx(mt=mt, x=x, i=i, g=g, defer=n, method=method)


def nAEx_(mt, x, n, i=None, g=.0, method='udd'):
    """
    Endowment insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of an Endowment life insurance (i.e. net single premium), that
    pays 1, at the moment of death or 1 if x survives to age x+n. It is also commonly referred to as the
    Actuarial Value or Actuarial Present Value.
    """
    return nAx_(mt=mt, x=x, n=n, i=i, g=g, method=method) + annuities.nEx(mt=mt, x=x, i=i, g=g, defer=n, method=method)


# deferred life insurances
def t_Ax(mt, x, defer=0, i=None, g=.0, method='udd'):
    """
    Deferred Whole life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1,at the
    end of the year of death. It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """

    return A_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=mt.w + 1, i=i, g=g, method=method)


def t_Ax_(mt, x, defer=0, i=None, g=.0, method='udd'):
    """
    Deferred Whole life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1,at the
    end of the year of death. It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """
    return t_Ax(mt=mt, x=x, defer=defer, i=i, g=g, method=method) * np.sqrt(1 + i / 100)


def t_nAx(mt, x, n, defer=0, i=None, g=.0, method='udd'):
    """
    Deferred Term life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a term (temporary) life insurance (i.e. net single premium), that
    pays 1, at the end of the year of death. It is also commonly referred to as the Actuarial Value or
    Actuarial Present Value.
    """
    return A_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=x + n + defer, i=i, g=g, method=method)


def t_nAx_(mt, x, n, defer=0, i=None, g=.0, method='udd'):
    """
    Deferred Term life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a term (temporary) life insurance (i.e. net single premium), that
    pays 1, at the end of the year of death. It is also commonly referred to as the Actuarial Value or
    Actuarial Present Value.
    """
    return t_nAx(mt=mt, x=x, n=n, defer=defer, i=i, g=g, method=method) * np.sqrt(1 + i / 100)


def t_nAEx(mt, x, n, defer=0, i=None, g=.0, method='udd'):
    """
    Deferred Endowment insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of an Endowment life insurance (i.e. net single premium), that
    pays 1, at the end of year of death or 1 if x survives to age x+n. It is also commonly referred to as the
    Actuarial Value or Actuarial Present Value.

    """
    return A_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=x + n + defer, i=i, g=g, method=method) + \
           annuities.nEx(mt=mt, x=x, i=i, g=g, defer=n + defer, method=method)


def t_nAEx_(mt, x, n, defer=0, i=None, g=.0, method='udd'):
    """
    Deferred Endowment insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param g: growth rate (flat rate) in percentage, e.g., 2 for 2%
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of an Endowment life insurance (i.e. net single premium), that
    pays 1, at the moment of death or 1 if x survives to age x+n. It is also commonly referred to as the
    Actuarial Value or Actuarial Present Value.

    """
    return A_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=x + n + defer, i=i, g=g, method=method)*np.sqrt(1+i/100) + \
           annuities.nEx(mt=mt, x=x, i=i, g=g, defer=n + defer, method=method)
