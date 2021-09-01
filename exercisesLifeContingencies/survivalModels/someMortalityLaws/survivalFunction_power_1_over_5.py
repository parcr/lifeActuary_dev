import numpy as np
import matplotlib.pyplot as plt
import os
import sys


def F0(t):
    if t < 0:
        return .0
    elif 0 <= t <= 105:
        return 1 - (1 - t / 105) ** (1 / 5)
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
    elif x >= 105:
        return np.inf
    else:
        return 1 / (525 - 5 * x)


'''
the probability that a newborn life dies before age 60,
'''
print(round(F0(60), 5))
'''
the probability that a life aged 30 survives to at least age 70,
'''
print(round(pxt(x=30, t=40), 5))
'''
the probability that a life aged 20 dies between ages 90 and 100,
'''
print(round(pxt(x=20, t=70) * qxt(x=90, t=10), 5))
'''
the force of mortality at age 50
'''
print(round(mu(x=50), 5))
'''
the median future lifetime at age 50,
'''
print(55*(1-2**-5))

'''
the curtate expectation of life at age 50.
'''
px_s=[pxt(50, t) for t in range(1,55)]
print(round(sum(px_s), 5))


'''graphs'''
x = np.arange(0, 105, .01)
cdf = [F0(t) for t in x]
surv = 1 - np.array(cdf)

plt.figure(figsize=(15, 4))
plt.subplot(1, 2, 1)
plt.plot(x, surv)
plt.title('Survival Function')
plt.xlabel('x')
plt.ylabel('')

plt.subplot(1, 2, 2)
plt.plot(x, cdf)
plt.title('Cumulative Distribution Function')
plt.xlabel('x')
plt.ylabel('')
plt.tight_layout()

this_py = os.path.split(sys.argv[0])[-1][:-3]
plt.savefig(this_py + '.eps', format='eps', dpi=3600)
plt.show()
