import numpy as np
from plotCDF.discrete import messages as msn


def support(s):
    try:
        s_ = np.asarray(s, dtype=np.float64)
        s_ = np.sort(s_)
    except ValueError as ve:
        raise ValueError(msn.needs_array + ' ' + str(ve))

    if s_.ndim != 1:
        raise TypeError(msn.needs_1_dim_array)
    elif s_.size == 1:
        raise TypeError(msn.needs_more_than_1)
    else:
        return s_


def prob(p, tol):
    p_ = support(p)
    sum_p = sum(p_)
    if sum(p_ <= 0) > 0:
        raise ValueError(msn.needs_all_positive)
    elif sum_p > 1. + tol:
        message = is_sum_probs_tol(p, tol)
        if sum_p > 1:
            print(f'The sum of the probabilities is {sum_p}>1.')
        if str:
            message = (msn.needs_lesser_1 + ' ' + message).strip()
            raise ValueError(message)
    else:
        return p_


def comp_supp_prob(s, p):
    if s is not None and p is not None:
        if len(s) != len(p):
            raise TypeError(msn.needs_same_size)
    return True


def is_sum_probs_tol(p, tol):
    sum_p = sum(p)
    if abs(sum_p - 1) > tol:
        if sum_p - 1 < 0:
            message = ' The error is ' + str(1 - sum_p) + ' with a tolerance of ' + str(tol) + '.'
            return msn.sum_of_prob + message
        else:
            str_sum_p = str(sum_p)
            str_error_sum_p = str(1. - sum_p)
            return 'The sum of probabilities is ' + str_sum_p + ' with an error of ' + str_error_sum_p + \
                   ' for a max. tolerance of ' + str(tol)
    return ''


def tolerance(t):
    if t > 1 or t < 0:
        raise ValueError(msn.tolerance)
    return t


def tail(t):
    if not type(t) == bool:
        raise TypeError(msn.tails)
    return t


def is_pmf(t):
    if not type(t) == bool:
        raise TypeError(msn.is_pmf)
    return t
