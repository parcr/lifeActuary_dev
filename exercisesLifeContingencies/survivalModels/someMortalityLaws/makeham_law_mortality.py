import numpy as np
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]


def mu(a, b, c, x):
    if x < 0 or a < 0 or (b <= 0 or b >= 1) or c <= 1:
        return np.nan
    return a + b * np.power(c, x)


def S(a, b, c, x, t):
    if x < 0 or a < 0 or (b <= 0 or b >= 1) or c <= 1:
        return np.nan
    if t < 0:
        return 1
    else:
        return np.exp(-b / np.log(c) * np.power(c, x) * (np.power(c, t) - 1)) * np.exp(-a * t)


def pdf(a, b, c, x, t):
    if x < 0 or a < 0 or (b <= 0 or b >= 1) or c <= 1:
        return np.nan
    if t < 0:
        return 1
    else:
        return (a + b * np.power(c, x + t)) * np.exp(-b / np.log(c) * np.power(c, x) * (np.power(c, t) - 1)) * np.exp(
            -a * t)


t = np.linspace(0, 100, 1000 + 1)
a = 0.0001
b = 0.00035
c = 1.075
x_s = [0, 20, 50, 80]

S_vec = np.vectorize(S)
fig, ax = plt.subplots()
for x in x_s:
    y = S_vec(a=a, b=b, c=c, x=x, t=t)
    plt.plot(t, y, label=f'x={x}')

plt.title(f'Makeham Law Survival Function (A={a}, B={b}, c={c})')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('t')
plt.ylabel(f'$S_x(t)$')
this_py = os.path.split(sys.argv[0])[-1][:-3]
plt.savefig(this_py + '_sf' + '.eps', format='eps', dpi=3600)
plt.show()

pdf_vec = np.vectorize(pdf)
fig, ax = plt.subplots()
for x in x_s:
    y = pdf_vec(a=a, b=b, c=c, x=x, t=t)
    plt.plot(t, y, label=f'x={x}')

plt.title(f'Makeham Law Probability Density Function (A={a}, B={b}, c={c})')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('t')
plt.ylabel(f'$f_x(t)$')
plt.savefig(this_py + '_pdf' + '.eps', format='eps', dpi=3600)
plt.show()

'''
Compute Life Table
'''

px = np.array([S(a, b, c, x, t=1) for x in range(0, 130 + 1)])
qx = 1 - px
lt = mortality_table.MortalityTable(mt=list(np.append(0, qx)))
lt.df_life_table().to_excel(excel_writer='makeham' + '.xlsx', sheet_name='makeham',
                            index=False, freeze_panes=(1, 1))

'''
Plot ex
'''
fig, axes = plt.subplots()
plt.plot(range(lt.x0, lt.w + 1), lt.ex, label=f'Makeham({a}, {b}, {c})')

plt.xlabel(r'$x$')
plt.ylabel(r'${e}_{x}+1/2$')
plt.title('Complete Expectation of Life')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_ex' + '.eps', format='eps', dpi=3600)
plt.show()

'''
Plot t|q_70
'''

t_s = np.array(range(0, lt.w - 70))
t_1q70 = [S(a, b, c, x=70, t=t) - S(a, b, c, x=70, t=t + 1) for t in t_s]

fig, axes = plt.subplots()
plt.plot(t_s + 70, t_1q70, label=f'Makeham({a}, {b}, {c})')

plt.xlabel(r'$x$')
plt.ylabel(r'$P(K_{70}=k)$')
plt.title(r'$_{t|}q_{70}$')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + 'pk70' + '.eps', format='eps', dpi=3600)
plt.show()
