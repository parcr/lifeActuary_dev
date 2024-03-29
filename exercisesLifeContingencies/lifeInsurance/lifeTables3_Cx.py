import numpy as np
import os
import sys

from soa_tables import read_soa_table_xml as rst
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=4, g=0, mt=mt.table_qx) for mt in mt_lst]

for idx, lt in enumerate(lt_lst):
    name = parse_table_name(mt_lst[idx].name)
    lt.df_life_table().to_excel(excel_writer=name + '.xlsx', sheet_name=name,
                                index=False, freeze_panes=(1, 1))
    ct_lst[idx].df_commutation_table().to_excel(excel_writer=name + '_comm' + '.xlsx', sheet_name=name,
                                                index=False, freeze_panes=(1, 1))

'''
Plot ex
'''
fig, axes = plt.subplots()
for idx, lt in enumerate(lt_lst):
    ages = np.arange(0, lt.w + 1)
    plt.plot(ages, lt.ex, label=table_names[idx])

plt.xlabel(r'$x$')
plt.ylabel(r'${e}_{x}+1/2$')
plt.title('Complete Expectation of Life')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '.eps', format='eps', dpi=3600)
plt.show()

'''
Plot ln(Dx)
'''
fig, axes = plt.subplots()
for idx, lt in enumerate(ct_lst):
    ages = np.arange(0, lt.w + 1)
    plt.plot(ages, np.log(lt.Dx), label=table_names[idx])

plt.xlabel(r'$x$')
plt.ylabel(r'$ln(D_x)$')
plt.title(r'ln(D_x)')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_comm1' + '.eps', format='eps', dpi=3600)
plt.show()


'''
Plot ln(Cx)
'''
fig, axes = plt.subplots()
for idx, lt in enumerate(ct_lst):
    ages = np.arange(0, lt.w + 1)
    plt.plot(ages, np.log(lt.Cx), label=table_names[idx])

plt.xlabel(r'$x$')
plt.ylabel(r'$ln(C_x)$')
plt.title(r'ln(C_x)')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
plt.savefig(this_py + '_comm2' + '.eps', format='eps', dpi=3600)
plt.show()


