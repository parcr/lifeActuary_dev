import lifecontingencies as lc
import numpy as np


# Whole life insurance ---
def r_Ax(mt, x, m=1, k=0, c=1):
    """ Ax : Returns the Expected Present Value (EPV) of a whole life insurance (i.e. net single premium).
    It is also commonly referred to as the Actuarial Value or Actuarial Present Value.
    m is the number of terms for the premium,
    k is the policy year,
    c is the capital"""
    an = (mt.Nx[x] - mt.Nx[x + m]) / mt.Dx[x]
    pr = mt.Mx[x] / (mt.Nx[x] - mt.Nx[x + m]) / (1 + mt.i) ** (0.5)
    if k <= m:
        return c * (mt.Mx[x + k] / mt.Dx[x + k] / (1 + mt.i) ** (0.5) - \
                    pr * (mt.Nx[x + k] - mt.Nx[x + m]) / mt.Dx[x + k])
    else:
        return c * mt.Mx[x + k] / mt.Dx[x + k] / (1 + mt.i) ** (0.5)


def v_r_Ax(mt, x, m=1, c=1):
    w = mt.w + 1
    reserves = np.zeros(shape=(w - x, 3))
    for j in range(x, w):
        reserves[j - x, 0] = int(j - x)
        reserves[j - x, 1] = int(j)
        reserves[j - x, 2] = np.round(r_Ax(mt=mt, x=x, m=m, k=j - x, c=c), 5)
    return reserves


# Term insurance ---
def r_Axn(mt, x, n, m=1, k=0, c=1):
    """ (A^1)x:n : Returns the EPV (net single premium) of a term insurance.
    m is the number of terms for the premium,
    k is the policy year,
    c is the capital"""
    an = (mt.Nx[x] - mt.Nx[x + m]) / mt.Dx[x]
    pr = (mt.Mx[x] - mt.Mx[x + n]) / (mt.Nx[x] - mt.Nx[x + m]) / (1 + mt.i) ** (0.5)
    if k <= m and m <= n and x + k <= x + n:
        return c * ((mt.Mx[x + k] - mt.Mx[x + n]) / mt.Dx[x + k] / (1 + mt.i) ** (0.5) - \
                    pr * (mt.Nx[x + k] - mt.Nx[x + m]) / mt.Dx[x + k])
    elif k > m and m <= n and x + k <= x + n:
        return c * (mt.Mx[x + k] - mt.Mx[x + n]) / mt.Dx[x + k] / (1 + mt.i) ** (0.5)
    else:
        return 0.


def v_r_Axn(mt, x, n, m=1, c=1):
    w = min(mt.w + 1, x + n + 1)
    reserves = np.zeros(shape=(w - x, 3))
    for j in range(x, w):
        reserves[j - x, 0] = int(j - x)
        reserves[j - x, 1] = int(j)
        reserves[j - x, 2] = np.round(r_Axn(mt=mt, x=x, n=n, m=m, k=j - x, c=c), 5)
    return reserves


# Pure endowment: Deferred capital ---
def r_nEx(mt, x, n, m=1, k=0, c=1):
    """ nEx : Returns the EPV of a pure endowment (deferred capital).
    Pure endowment benefits are conditional on the survival of the policyholder. (v^n * npx)
    m is the number of terms for the premium,
    k is the policy year,
    c is the capital"""
    w = min(mt.w + 1, x + n + 1)
    reserves = np.zeros(shape=(w - x, 3))
    an = (mt.Nx[x] - mt.Nx[x + m]) / mt.Dx[x]
    pr = mt.Dx[x + n] / (mt.Nx[x] - mt.Nx[x + m])
    if k <= m and m <= n and x + k <= x + n:
        return c * (mt.Dx[x + n] / mt.Dx[x + k] - \
                    pr * (mt.Nx[x + k] - mt.Nx[x + m]) / mt.Dx[x + k])
    elif k > m and m <= n and x + k <= x + n:
        return c * mt.Dx[x + n] / mt.Dx[x + k]
    else:
        return 0.


def v_r_nEx(mt, x, n, m=1, c=1):
    w = min(mt.w + 1, x + n + 1)
    reserves = np.zeros(shape=(w - x, 3))
    for j in range(x, w):
        reserves[j - x, 0] = int(j - x)
        reserves[j - x, 1] = int(j)
        reserves[j - x, 2] = np.round(r_nEx(mt=mt, x=x, n=n, m=m, k=j - x, c=c), 5)
    return reserves


# Endowment insurance ---
def r_AExn(mt, x, n, m=1, k=0, c_d=1, c_s=1):
    """ AExn : Returns the EPV of a endowment insurance.
    An endowment insurance provides a combination of a term insurance and a pure endowment
    m is the number of terms for the premium,
    k is the policy year,
    c_d is the capital in case of death
    c_s is the capital in case of survival """
    return r_Axn(mt=mt, x=x, n=n, m=m, k=k, c=c_d) + \
           r_nEx(mt=mt, x=x, n=n, m=m, k=k, c=c_s)


def v_r_AExn(mt, x, n, m=1, c_d=1, c_s=1):
    w = min(mt.w + 1, x + n + 1)
    reserves = np.zeros(shape=(w - x, 5))
    for j in range(x, w):
        reserves[j - x, 0] = int(j - x)
        reserves[j - x, 1] = int(j)
        reserves[j - x, 2] = np.round(r_Axn(mt=mt, x=x, n=n, m=m, k=j - x, c=c_d), 5)
        reserves[j - x, 3] = np.round(r_nEx(mt=mt, x=x, n=n, m=m, k=j - x, c=c_s), 5)
        reserves[j - x, 4] = np.round(r_Axn(mt=mt, x=x, n=n, m=m, k=j - x, c=c_d) + \
                                      r_nEx(mt=mt, x=x, n=n, m=m, k=j - x, c=c_s), 5)
    return reserves
