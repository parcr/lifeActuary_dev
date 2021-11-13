import numpy as np
import matplotlib.pyplot as plt
import os
import sys


def F0(t):
    if t < 0:
        return .0
    elif 0 <= t <= 120:
        return 1 - (1 - t / 120) ** (1 / 6)
    else:
        return 1.


def S0(t):
    return 1 - F0(t)


def pxt(x, t):
    if t <= 0:
        return 1
    try:
        return S0(x + t) / S0(x)
    except ZeroDivisionError:
        return .0


def qxt(x, t):
    return 1 - pxt(x, t)


def mu(x):
    if x < 0:
        return .0
    elif x >= 125:
        return np.inf
    else:
        return 0  # 1 / (525 - 5 * x)


'''
The probability of $(25)$ dying before complete 50 year old.
'''
print(round(qxt(25, 25), 5))

'''
$\px[5]{45}$
'''
print(round(pxt(45, 5), 5))

'''
$\qx[5|2]{45}=\px[5]{45}\:\qx[2]{47}
'''
print(round(pxt(45, 5) * qxt(50, 2), 5))

'''
E(K_{118})
'''
probs = [pxt(118, t) for t in range(1, 3)]
print(round(sum(probs), 5))
