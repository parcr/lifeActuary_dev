from essential_life import mortality_table
from soa_tables import read_soa_table_xml as rst
import pandas as pd

# reads soa table
soa = rst.SoaTable('../soa_tables/' + 'TV7377' + '.xml')
table_manual_qx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='qx')
table_manual_lx = pd.read_excel('../soa_tables/' + 'tables_manual' + '.xlsx', sheet_name='lx')

# creates mortality table from 1x of soa table
tv7377 = mortality_table.MortalityTable(data_type='q', mt=soa.table_qx, perc=100, last_q=1)
grf95 = mortality_table.MortalityTable(data_type='q', mt=list(table_manual_qx['GRF95']), perc=100, last_q=1)
grm95 = mortality_table.MortalityTable(data_type='l', mt=list(table_manual_lx['GRM95']), perc=100, last_q=1)

print('Some Tests')
x = 17.5
print(tv7377.lx_bal(x))
print(tv7377.lx_cfm(x))
print(tv7377.lx_udd(x))

print()
x0 = 17.5
n0 = 62.5
lst_npx = [grf95.npx(x=x0, n=n0, method=m) for m in grf95.methods]
lst_npx_2 = [grf95.npx(x=int(x0), n=int(n0), method=m) for m in grf95.methods]

print(lst_npx)
print(lst_npx_2)
