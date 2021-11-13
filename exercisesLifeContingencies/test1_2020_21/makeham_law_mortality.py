from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]
# mml = makeham_mortality_functions.Makeham(a=0.0001, b=0.0003, c=1.07)
mml = makeham_mortality_functions.Makeham(a=0.0001, b=0.00035, c=1.075)
interest_rate = 4

e0 = mml.moments_Tx()
e70 = mml.moments_Tx(x=70)

'''
Compute Life Table
'''
w = 125
px = np.array([mml.S(x, t=1) for x in range(0, w)])
qx = 1 - px
lt = mortality_table.MortalityTable(mt=list(np.append(0, qx)))
w = len(px)
ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=list(np.append(0, qx)))

'''
lt.df_life_table().to_excel(excel_writer='makeham_' + str(w) + '.xlsx', sheet_name='makeham',
                            index=False, freeze_panes=(1, 1))
ct.df_commutation_table().to_excel(excel_writer='makeham' + '_comm_' + str(w) + '.xlsx', sheet_name='makeham',
                                   index=False, freeze_panes=(1, 1))
'''

print(f'E(T_0)= {e0}')
print(f'E(T_70)= {e70}')
print(f'E(K_0)= {lt.ex[0] - .5}')
print(f'E(K_70)= {lt.ex[70] - .5}')

'''a'''
capital = 10000
x = 55
t = 10
nEx = ct.nEx(x=x, n=t)
Dx = ct.Dx[x]
Nx_t = ct.Nx[x + t]
Dx_t = ct.Dx[x + t]
ax_t = Nx_t / Dx_t
renda = nEx * ax_t
renda_cap = capital * renda

renda_ct = ct.t_aax(x=x, m=1, defer=t)

print()
print(f'N=', round(Nx_t, 5))
print(f'D=', round(Dx, 5))
P1 = Nx_t / Dx
print(f'P1=', round(P1, 5))
P = capital * P1
print(f'P=', round(P, 2))

'''b'''
print()
level = 10
N_x1 = ct.Nx[x]
N_x2 = ct.Nx[x + level]
print('ann_level=', round((N_x1 - N_x2) / Dx, 5))
ann_level_ct = ct.naax(x=x, n=level, m=1)
print('ann_level_ct=', round(ann_level_ct, 5))
print('Pleveled=', round(P / ann_level_ct, 2))

'''c'''
x = 55
t = 10
term = 15
nEx = ct.nEx(x=x, n=t)
Dx = ct.Dx[x]
Nx_t = ct.Nx[x + t + 1]
Nx_t2 = ct.Nx[x + t + 1 + term]

renda2 =  (Nx_t - Nx_t2) / Dx
print('renda2=', round(renda2, 5))
renda2_ct = ct.t_nax(x=x, n=term, m=1, defer=10)
renda2_cap = capital * renda2
