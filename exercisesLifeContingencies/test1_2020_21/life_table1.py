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
interest_rate = 4
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

table_idx = 2
name = table_names[2]
lt = lt_lst[table_idx]
ct = ct_lst[table_idx]

lt.df_life_table().to_excel(excel_writer=name + '.xlsx', sheet_name=name,
                            index=False, freeze_panes=(1, 1))
ct.df_commutation_table().to_excel(excel_writer=name + '_comm' + '.xlsx', sheet_name=name,
                                   index=False, freeze_panes=(1, 1))

x = 55
defer = 10
temp = 15
renda = ct.t_naax(x=x, n=temp, m=12, defer=defer)
print(f'renda frac=', renda)
print(f'capital frac=', renda*12000)