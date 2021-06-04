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
first_instalment_at = 5
number_of_instalments = 1000
instalment = 10000
x0 = 50
renda = ct.aax(x=x0)
# todo: change here to become generic; fund_0 = ct.aax(x=x0) * instalment * lx
dict_annuity = {'x': x0, 'm': 1, 'defer': first_instalment_at}
fund_0 = ct.t_aax(x=dict_annuity['x'], m=dict_annuity['m'], defer=dict_annuity['defer']) * instalment * lx
premium_instalments = 1
renda_aux = ct.naax(x=x0, n=premium_instalments)
premium1 = fund_0 / lx / renda_aux

i = interest_rate / 100
dict_liability = {'t': [], 'x': [], 'tpx': [], 'premium1': [], 'claim1': [],
                  'fund1': [], 'lx': [], 'premium': [], 'claim': [], 'fund': []}

dict_reserves = {'t': [], 'x': [], 'insured': [], 'insurer': [], 'reserve': [], 'fund': []}

for idx, x in enumerate(range(x0, lt.w + 1 + 1)):
    dict_liability['t'].append(idx)
    dict_liability['x'].append(x)
    dict_liability['tpx'].append(lt.tpx(x=x0, t=idx))
    if idx <= premium_instalments - 1:
        dict_liability['premium1'].append(dict_liability['tpx'][-1] * premium1)
    else:
        dict_liability['premium1'].append(.0)
    if idx >= first_instalment_at:
        dict_liability['claim1'].append(dict_liability['tpx'][-1] * instalment)
    else:
        dict_liability['claim1'].append(0)
    if idx == 0:
        dict_liability['fund1'].append(fund_0 / lx - dict_liability['claim1'][-1])
    else:
        dict_liability['fund1'].append(dict_liability['fund1'][-1] * (1 + i) - dict_liability['claim1'][-1])
    dict_liability['lx'].append(lx * dict_liability['tpx'][-1])
    dict_liability['premium'].append(dict_liability['premium1'][-1] * lx)
    dict_liability['claim'].append(dict_liability['claim1'][-1] * lx)
    dict_liability['fund'].append(dict_liability['fund1'][-1] * lx)

    # reserves
    if idx <= premium_instalments - 1:
        renda_aux = ct.naax(x=x0, n=premium_instalments - idx)
        dict_reserves['insured'].append(dict_liability['lx'][-1] * premium1 * renda_aux)
    else:
        dict_reserves['insured'].append(.0)
    renda_aux_2 = ct.t_aax(x=dict_annuity['x'] + idx, m=dict_annuity['m'],
                           defer=max(dict_annuity['defer'] - idx, 0))  # ct.aax(x=x0 + idx)
    dict_reserves['insurer'].append(dict_liability['lx'][-1] * renda_aux_2 * instalment)
    dict_reserves['reserve'].append(dict_reserves['insurer'][-1] - dict_reserves['insured'][-1])
    dict_reserves['fund'].append(dict_reserves['reserve'][-1] - dict_liability['claim'][-1])

dict_reserves['t'] = dict_liability['t']
dict_reserves['x'] = dict_liability['x']

df_liability = pd.DataFrame(dict_liability)
df_reserves = pd.DataFrame(dict_reserves)
path = 'amortization_scheme_annuity.xlsx'
# df_liability.to_excel('amortization_scheme_annuity' + '.xlsx', sheet_name='liability', index=False, freeze_panes=(1, 0))
# df_reserves.to_excel('reserves_annuity' + '.xlsx', sheet_name='reserves', index=False, freeze_panes=(1, 0))

writer = pd.ExcelWriter(path)
df_liability.to_excel(writer, sheet_name='liability', index=False, freeze_panes=(1, 0))
df_reserves.to_excel(writer, sheet_name='reserves', index=False, freeze_panes=(1, 0))
writer.save()
writer.close()
