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


def mu(x):
    if x < 0:
        return .0
    elif x >= 120:
        return np.inf
    else:
        return 1 / (720 - 6 * x)


def moments_Tx(x=0, k=1):
    if x < 0:
        return np.nan
    if x > 120:
        return 0
    if k == 0:
        return 1
    elif k == 1:
        return 6 / 7 * (120 - x)
    elif k == 2:
        return 72 / 91 * (120 - x) ** 2


def expected_value_Tx(x):
    return moments_Tx(x)


def variance_Tx(x):
    return moments_Tx(x=x, k=2) - moments_Tx(x=x, k=1) ** 2


def moments_Kx(x=0, k=1):
    if x < 0 or k < 0:
        return np.nan
    if k == 0:
        return 1
    elif k == 1:
        probs = [pxt(x=x, t=n) for n in range(1, int(120 - x + 1))]
        ev = np.sum(probs)
        return ev
    elif k == 2:
        probs = [pxt(x=x, t=n) for n in range(1, int(120 - x + 1))]
        ev = np.sum(probs)
        probs = [n * pxt(x=x, t=n) for n in range(1, int(120 - x + 1))]
        ev = k * np.sum(probs) - ev
        return ev


def expected_value_Kx(x=0):
    return moments_Kx(x=x, k=1)


def variance_Kx(x=0):
    ev = expected_value_Kx(x=x, )
    ev_square = moments_Kx(x=x, k=2)
    return ev_square - np.power(ev, 2)


x = np.arange(0, 120, .01)
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
plt.show()
this_py = os.path.split(sys.argv[0])[-1][:-3]
plt.savefig(this_py + '.eps', format='eps', dpi=3600)

''' 1 '''
print('a', S0(30))

''' 2 '''
print('b', (F0(50) - F0(30)) / S0(30))

''' 3 '''
print('c', S0(65) / S0(40))

'''
Compare q_x with \mu_x+.5
'''

mu_vec = np.vectorize(mu)
ages = np.linspace(0, 120, 121)
mu_s = mu_vec(x=ages + .5)
pxt_vec = np.vectorize(pxt)
qx = 1 - pxt_vec(x=ages, t=1)
error_qx = qx - mu_s
relat_error_qx = np.abs(error_qx / qx)

fig, ax = plt.subplots()
plt.plot(ages, qx, label=f'$q_x$')
plt.plot(ages, mu_s, label=f'$\mu_x$')
plt.title(f'Mortality Law $q_x$ versus $\mu_x$')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('t')
plt.ylabel(f'$q_x$ and $\mu_x$')
plt.savefig(this_py + '_qx_mu' + '.eps', format='eps', dpi=3600)
plt.show()

for a in [20, 50, 110]:
    print(f"$q_{{{a}}}$={qx[a]} versus $\mu_{{{a}+.5}}$={mu_s[a]}")

'''
Calculation of the Moments for T_x and K_x
'''

ev_s = [expected_value_Tx(a) for a in ages]
ev_K_s = [expected_value_Kx(a) for a in ages[:]]
fig, ax = plt.subplots()
plt.plot(ages, ev_s, label=f'$E(T_x)$')
plt.plot(ages, ev_K_s, label=f'$E(K_x)$')
plt.title(f'Complete Expectation of Life')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('x')
plt.ylabel(r'$E(T_x)$ and $E(K_x)$')
plt.savefig(this_py + '_ev_Tx' + '.eps', format='eps', dpi=3600)
plt.show()

ev_s = [variance_Tx(a) for a in ages]
ev_K_s = [variance_Kx(a) for a in ages]
fig, ax = plt.subplots()
plt.plot(ages, ev_s, label=r'$V(T_x)$')
plt.plot(ages, ev_K_s, label=r'$V(K_x)$')
plt.title(f'Variance for Future Lifetime')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('x')
plt.ylabel(r'$V(T_x)$ and $V(K_x)$')
plt.savefig(this_py + '_var_Tx' + '.eps', format='eps', dpi=3600)
plt.show()

for a in [0, 20, 30, 50, 80, 110]:
    print(f"$E(T_{{{a}}})$={expected_value_Tx(a)}" + ' and ' + f"$V(T_{{{a}}})$={variance_Tx(a)}")
    print(f"$E(K_{{{a}}})$={expected_value_Kx(a)}" + ' and ' + f"$V(K_{{{a}}})$={variance_Kx(a)}")
