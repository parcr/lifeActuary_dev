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
compute Whole Life Insurance with fraction for fraction ages using the survival function to compute 
the probabilities of non integer ages
'''

wli_12 = {'age': [], 'Ax_frac12': []}
# ages = range(ct.w + 1)
ages = np.arange(start=0, stop=ct.w + 1, step=1 / 12)
for idx, x in enumerate(ages):
    wli_12['age'].append(x)
    wli_12['Ax_frac12'].append(
        mml.life_insurance(x=x, interest_rate=5, age_first_instalment=x, terms=np.inf, fraction=12, w=129))
wli_12_df = pd.DataFrame(wli_12)
wli_12_df.to_excel(excel_writer='makeham_wli_12' + '.xlsx', sheet_name='makeham',
                            index=False, freeze_panes=(1, 1))

fig, axes = plt.subplots()
plt.plot(ages, wli_12['Ax_frac12'], label=f'Makeham({mml.a}, {mml.b}, {mml.c})')

plt.xlabel(r'$x$')
plt.ylabel(r'$A_x^{(12)}$')
plt.title(r'Whole Life Insurance $A_x^{(12)}$')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + 'Ax_12' + '.eps', format='eps', dpi=3600)
plt.show()
