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
    v = float((1 + g) / (1 + i))
    number_of_payments = int((x_last - x_first) + 1)
    payments_instants = np.linspace(x_first - x, x_last - x, number_of_payments)
    instalments = [mt.tpx(x, t=t - 1, method=method) * mt.tqx(x + t - 1, t=1, method=method) * np.power(v, t)
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
    return A_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=x + n + defer, i=i, g=g, method=method) * np.sqrt(
        1 + i / 100) + \
           annuities.nEx(mt=mt, x=x, i=i, g=g, defer=n + defer, method=method)


''' 
Situations of linear increment
'''


def IA_x(mt, x, x_first, x_last, i=None, inc=1., method='udd'):
    """
    Whole life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param x_first: age of first payment
    :param x_last: age of final payment
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1+m,at the
    end of the year of death, that pays 1+m, if death happens between age x+m and x+m+1.
    It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """
    if x_first < x: return np.nan
    if x_last < x_first == x: return np.nan
    if x == x_first == x_last: return 0
    i = i / 100
    i = float(1 / (1 + i))
    number_of_payments = int((x_last - x_first) + 1)
    payments_instants = np.linspace(x_first - x, x_last - x, number_of_payments)
    instalments = [mt.tpx(x, t=t - 1, method=method) * mt.tqx(x + t - 1, t=1, method=method) * np.power(i, t) *
                   ((t - (x_first - x)) * inc + 1) for t in payments_instants]
    instalments = np.array(instalments)
    return np.sum(instalments)


def IAx(mt, x, i=None, inc=1., method='udd'):
    """
    Whole life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1+m,at the
    end of the year of death, if death happens between age x+m and x+m+1.
    It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """

    return IA_x(mt=mt, x=x, x_first=x + 1, x_last=mt.w + 1, i=i, inc=inc, method=method)


def IAx_(mt, x, i=None, inc=1., method='udd'):
    """
    Whole life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1+m,at the
    moment of death, if death happens between age x+m and x+m+1.
    It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """

    return IAx(mt=mt, x=x, i=None, inc=inc, method=method) * np.sqrt(1 + i / 100)


def nIAx(mt, x, n, i=None, inc=1., method='udd'):
    """
    Whole life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1+m,at the
    end of the year of death, if death happens between age x+m and x+m+1.
    It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """

    return IA_x(mt=mt, x=x, x_first=x + 1, x_last=x + n, i=i, inc=inc, method=method)


def nIAx_(mt, x, n, i=None, inc=1., method='udd'):
    """
    Whole life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1+m, at the
    moment of death, if death happens between age x+m and x+m+1.
    It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """

    return nIAx(mt=mt, x=x, n=n, i=i, inc=inc, method=method) * np.sqrt(1 + i / 100)


def nIAEx(mt, x, n, i=None, inc=1, method='udd'):
    """
    Endowment insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of an Endowment life insurance (i.e. net single premium), that pays 1+m,
    at the end of year of death, if death happens between age x+m and x+m+1, or 1 if x survives to age x+n.
     It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """
    return nIAx(mt=mt, x=x, n=n, i=i, inc=inc, method=method) + \
           annuities.nEx(mt=mt, x=x, i=i, g=0, defer=n, method=method)


def nIAEx_(mt, x, n, i=None, inc=1, method='udd'):
    """
    Endowment insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of an Endowment life insurance (i.e. net single premium), that pays 1+m,
    at the moment of death, if death happens between age x+m and x+m+1, or 1 if x survives to age x+n.
     It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """
    return nIAx(mt=mt, x=x, n=n, i=i, inc=inc, method=method) * np.sqrt(1 + i / 100) + \
           annuities.nEx(mt=mt, x=x, i=i, g=0, defer=n, method=method)


# deferred life insurances
def t_IAx(mt, x, defer=0, i=None, inc=1., method='udd'):
    """
    Deferred Whole life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1, at the
    end of the year of death. It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """

    return IA_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=mt.w + 1, i=i, inc=inc, method=method)


def t_IAx_(mt, x, defer=0, i=None, inc=1., method='udd'):
    """
    Deferred Whole life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1, at the
    moment of death. It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """

    return t_IAx(mt=mt, x=x, defer=defer, i=i, inc=inc, method=method) * np.sqrt(1 + i / 100)


def t_nIAx(mt, x, n, defer=0, i=None, inc=1., method='udd'):
    """
    Deferred Term life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1+m, at the
    end of the year of death, if death happens between age x+m and x+m+1.
    It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """
    return IA_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=x + n + defer, i=i, inc=inc, method=method)


def t_nIAx_(mt, x, n, defer=0, i=None, inc=1., method='udd'):
    """
    Deferred Term life insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1+m, at the
    moment of death, if death happens between age x+m and x+m+1.
    It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """
    return t_nIAx(mt=mt, x=x, n=n, defer=defer, i=i, inc=inc, method=method) * np.sqrt(1 + i / 100)


def t_nIAEx(mt, x, n, defer=0, i=None, inc=1., method='udd'):
    """
    Deferred Endowment insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1+m, at the
    end of the year of death, if death happens between age x+m and x+m+1 or 1 if x survives to age x+n+defer.
    It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """
    return IA_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=x + n + defer, i=i, inc=inc, method=method) + \
           annuities.nEx(mt=mt, x=x, i=i, g=0, defer=n + defer, method=method)


def t_nIAEx_(mt, x, n, defer=0, i=None, inc=1., method='udd'):
    """
    Deferred Endowment insurance
    :param mt: table for life x
    :param x: age at the beginning of the contract
    :param n: period of the contract
    :param defer: deferment period
    :param i: technical interest rate (flat rate) in percentage, e.g., 2 for 2%
    :param inc: linear increment in monetary units, e.g., 1 for one monetary unit
    :param method: the method to approximate the fractional periods
    :return: Expected Present Value (EPV) of a whole life insurance (i.e. net single premium), that pays 1+m, at the
    end of the year of death, if death happens between age x+m and x+m+1 or 1 if x survives to age x+n+defer.
    It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    """
    return IA_x(mt=mt, x=x, x_first=x + 1 + defer, x_last=x + n + defer, i=i, inc=inc, method=method) * \
           np.sqrt(1 + i / 100) + annuities.nEx(mt=mt, x=x, i=i, g=0, defer=n + defer, method=method)
