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
    return 1 - ((120 + t) / 120) ** (-2)


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
    else:
        return (120 / (120 + x)) / 60


'''
\item The probability of $(25)$ dying before attaining 65 years old. %1.0
'''
print(round(qxt(25, 40), 10))

'''
\item $\px[10]{55}$. %1.0
'''
print(round(pxt(55, 10), 10))

'''
$\qx[10|5]{45}=\px[45]{10}\:\qx[5]{55}
'''
print(round(pxt(45, 10) * qxt(55, 5), 10))

'''some graphs'''
x_s = np.linspace(0, 120, 1000)

''' Ln force of mortality'''
force_of_motality_lst = [mu(t) for t in x_s]
fig, axes = plt.subplots()
plt.plot(x_s, np.log(force_of_motality_lst), label=f' ln Mortality Force({0}, {120})')
plt.xlabel(r'$x$')
plt.ylabel(r'$\mu_{x}$')
plt.title(r'ln Force of Mortality')
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

'''
Note this is not a good survival function because the probabilities of surviving one year are increasing
'''
lst_1px = [(x, pxt(x, 1)) for x in range(0, 120 + 1)]
