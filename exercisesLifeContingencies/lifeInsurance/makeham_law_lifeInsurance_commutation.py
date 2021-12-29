import pandas as pd
from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]
mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)

e0 = mml.moments_Tx()

'''
Compute Life Table
'''
interest_rate = 5
px = np.array([mml.S(x, t=1) for x in range(0, 128 + 1)])
qx = 1 - px
lt = mortality_table.MortalityTable(mt=list(np.append(0, qx)))
lt.df_life_table().to_excel(excel_writer='makeham' + '.xlsx', sheet_name='makeham',
                            index=False, freeze_panes=(1, 1))
ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=list(np.append(0, qx)))
ct.df_commutation_table().to_excel(excel_writer='makeham' + '_comm' + '.xlsx', sheet_name='makeham',
                                   index=False, freeze_panes=(1, 1))

'''
compute Whole Life Insurance using Commutation Functions
'''

# wli = [[age, ct.Ax(age)] for age in range(ct.w + 1)]
wli = {'age': [], 'Ax': []}
ages = range(ct.w + 1)
for idx, x in enumerate(ages):
    wli['age'].append(x)
    wli['Ax'].append(ct.Ax(x))
wli_df = pd.DataFrame(wli)
wli_df.to_excel(excel_writer='makeham_wli' + '.xlsx', sheet_name='makeham_wli',
                index=False, freeze_panes=(1, 1))

fig, axes = plt.subplots()
plt.plot(ages, wli['Ax'], label=f'Makeham({mml.a}, {mml.b}, {mml.c})')

plt.xlabel(r'$x$')
plt.ylabel(r'$A_x$')
plt.title(r'Whole Life Insurance $A_x$')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + 'Ax' + '.eps', format='eps', dpi=3600)
plt.show()

'''
compute Whole Life Insurance for fraction ages using the commutation symbols to compute 
the probabilities of non integer ages
'''

''' commutation table '''
m = 12
ages = np.arange(start=0, stop=ct.w + 1, step=1 / m)
surv_probs = [(idx_a, a, mml.S(x=a, t=1 / m)) for idx_a, a in enumerate(ages)]

px = np.array([mml.S(x=a, t=1 / m) for idx_a, a in enumerate(ages)])
qx = 1 - px
tpx = np.cumprod(px)
l0 = lt.lx[0]
lx = np.append(l0, l0 * tpx)
lx = lx[:-1]
v_m = (1 + interest_rate / 100) ** (-1 / m)
Dx = lx[:] * np.power(v_m, range(len(lx[:])))
Nx = np.array([np.sum(Dx[x:]) for x in range(len(lx[:]))])
Sx = np.array([np.sum(Nx[x:]) for x in range(len(Nx))])
dx = np.append(lx[:-1] - lx[1:], lx[-1])

Cx = dx * np.power(v_m, range(len(lx[:]))) * v_m
Mx = np.array([np.sum(Cx[x:]) for x in range(len(lx[:]))])
Rx = np.array([np.sum(Mx[x:]) for x in range(len(lx[:]))])

wli_m = {'age': ages, 'lx': lx, 'dx': dx, 'qx': qx, 'px': px, 'Dx': Dx, 'Nx': Nx, 'Sx': Sx, 'Cx': Cx, 'Mx': Mx,
         'Rx': Rx}

wli_m_df = pd.DataFrame(wli_m)
wli_m_df.to_excel(excel_writer=f'makeham_wli_comm_{m}' + '.xlsx', sheet_name=f'makeham_wli_{m}',
                  index=False, freeze_panes=(1, 1))

fig, axes = plt.subplots()
plt.plot(ages, Mx / Dx, label=f'Makeham({mml.a}, {mml.b}, {mml.c})_{m}')

plt.xlabel(r'$x$')
plt.ylabel(r'$A_x^{(m)}$')
plt.title(r'Whole Life Insurance $A_x^{m}$')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + f'Ax_{m}' + '.eps', format='eps', dpi=3600)
plt.show()

''' Compare plots '''
ages_int = range(ct.w + 1)
fig, axes = plt.subplots()
plt.plot(ages, Mx / Dx, label=f'Makeham({mml.a}, {mml.b}, {mml.c})_{m}')
plt.plot(ages_int, wli['Ax'], label=f'Makeham({mml.a}, {mml.b}, {mml.c})')

plt.xlabel(r'$x$')
plt.ylabel(r'$A_x^{(m)}$ and $A_x$')
plt.title(r'Whole Life Insurance')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + f'Ax_s' + '.eps', format='eps', dpi=3600)
plt.show()
