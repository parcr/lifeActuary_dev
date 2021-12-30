import numpy as np
import matplotlib.pyplot as plt
import os
import sys

import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]


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
        return 1 / (720-6 * x)


'''
The probability of $(25)$ dying before complete 50 year old.
'''
print(round(qxt(25, 25), 10))

'''
$\px[5]{45}$
'''
print(round(pxt(45, 5), 10))

'''
$\qx[5|2]{45}=\px[5]{45}\:\qx[2]{47}
'''
print(round(pxt(45, 5) * qxt(50, 2), 10))

'''
E(K_{118})
'''
probs = [pxt(118, t) for t in range(1, 3)]
print(round(sum(probs), 10))

'''some graphs'''
x_s = np.linspace(0, 120, 1000)

''' Ln force of mortality'''
force_of_motality_lst = [mu(t) for t in x_s]
fig, axes = plt.subplots()
plt.plot(x_s, np.log(force_of_motality_lst), label=f'Mortality Force({0}, {120})')
plt.xlabel(r'$x$')
plt.ylabel(r'$\mu_{x}$')
plt.title(r'Force of Mortality')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_force_of_mortality' + '.eps', format='eps', dpi=3600)
plt.show()

''' Survival Function '''
prob_survival_lst = [S0(t) for t in x_s]
fig, axes = plt.subplots()
plt.plot(x_s, prob_survival_lst, label=f'Survival Function({0}, {120})')
plt.xlabel(r'$x$')
plt.ylabel(r'$S_{0}(x)$')
plt.title(r'Survival Function')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_Survival_Function' + '.eps', format='eps', dpi=3600)
plt.show()