import pandas as pd

from soa_tables import read_soa_table_xml as rst
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt

table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 4
name = table_names[0]
mt = rst.SoaTable('../../soa_tables/' + name + '.xml')
lt = mortality_table.MortalityTable(mt=mt.table_qx)
ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx)

lx = 1000
frequency = 1
instalment = 1000
x0 = 60
renda = ct.aax(x=x0)
fund_0 = ct.aax(x=x0) * instalment * lx

i = interest_rate / 100
dict_liability = {'t': [], 'x': [], 'tpx': [], 'EV_payment': [],
                  'EV_fund1': [], 'EV_lx': [], 'EV_fund': []}

dict_fund = {'C_t': [instalment], 'j': [0], 'In': [0], 'Out': []}

for idx, x in enumerate(range(x0, lt.w + 1 + 1)):
    dict_liability['t'].append(idx)
    dict_liability['x'].append(x)
    dict_liability['tpx'].append(lt.tpx(x=x0, t=idx))
    dict_liability['EV_payment'].append(dict_liability['tpx'][-1] * instalment)
    if idx == 0:
        dict_liability['EV_fund1'].append(fund_0 / lx)
    else:
        dict_liability['EV_fund1'].append(dict_liability['EV_fund1'][-1] * (1 + i) - dict_liability['EV_payment'][-1])
    dict_liability['EV_lx'].append(lx * dict_liability['tpx'][-1])
    dict_liability['EV_fund'].append(dict_liability['EV_fund1'][-1] * lx)

df_fund = pd.DataFrame(dict_liability)
