from soa_tables import read_soa_table_xml as rst
from essential_life import mortality_table, commutation_table
import pandas as pd


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]

for idx, lt in enumerate(lt_lst):
    name = parse_table_name(mt_lst[idx].name)
    lt.df_life_table().to_excel(excel_writer=name+'.xlsx', sheet_name=name,
                                index=False, freeze_panes=(1, 1))


#todo: prepare commutation functions
'''
cf_tv7377 = commutation_table.CommutationFunctions(i=1.4, g=1, mt=mt_TV7377.table_qx)
cf_grf95 = commutation_table.CommutationFunctions(i=1.4, g=1, mt=mt_GRF95.table_qx)
cf_grm95 = commutation_table.CommutationFunctions(i=1.4, g=1, mt=mt_GRM95.table_qx)
'''