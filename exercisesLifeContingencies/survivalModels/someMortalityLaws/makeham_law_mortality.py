from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]
mml = makeham_mortality_functions.Makeham(a=0.0001, b=0.00035, c=1.075)

e0 = mml.moments_Tx()

t = np.linspace(0, 100, 1000 + 1)
x_s = [0, 20, 50, 80]

S_vec = np.vectorize(mml.S)
fig, ax = plt.subplots()
for x in x_s:
    y = S_vec(x=x, t=t)
    plt.plot(t, y, label=f'x={x}')

plt.title(f'Makeham Law Survival Function (A={mml.a}, B={mml.b}, c={mml.c})')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('t')
plt.ylabel(f'$S_x(t)$')
this_py = os.path.split(sys.argv[0])[-1][:-3]
plt.savefig(this_py + '_sf' + '.eps', format='eps', dpi=3600)
plt.show()

pdf_vec = np.vectorize(mml.pdf)
fig, ax = plt.subplots()
for x in x_s:
    y = pdf_vec(x=x, t=t)
    plt.plot(t, y, label=f'x={x}')

plt.title(f'Makeham Law Probability Density Function (A={mml.a}, B={mml.b}, c={mml.c})')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.xlabel('t')
plt.ylabel(f'$f_x(t)$')
plt.savefig(this_py + '_pdf' + '.eps', format='eps', dpi=3600)
plt.show()

'''
Compute Life Table
'''
interest_rate = 4
px = np.array([mml.S(x, t=1) for x in range(0, 110 + 1)])
qx = 1 - px
lt = mortality_table.MortalityTable(mt=list(np.append(0, qx)))
w = len(px)-1
lt.df_life_table().to_excel(excel_writer='makeham_' + str(w) + '.xlsx', sheet_name='makeham',
                            index=False, freeze_panes=(1, 1))
ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=list(lt.qx))
ct.df_commutation_table().to_excel(excel_writer='makeham' + '_comm_' + str(w) + '.xlsx', sheet_name='makeham',
                                   index=False, freeze_panes=(1, 1))

'''
Plot ex
'''
fig, axes = plt.subplots()
plt.plot(range(lt.x0, lt.w + 1), lt.ex, label=f'Makeham({mml.a}, {mml.b}, {mml.c})')

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
t_1q70 = [mml.S(x=70, t=t) - mml.S(x=70, t=t + 1) for t in t_s]

fig, axes = plt.subplots()
plt.plot(t_s + 70, t_1q70, label=f'Makeham({mml.a}, {mml.b}, {mml.c})')

plt.xlabel(r'$x$')
plt.ylabel(r'$P(K_{70}=k)$')
plt.title(r'$_{t|}q_{70}$')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + 'pk70' + '.eps', format='eps', dpi=3600)
plt.show()
