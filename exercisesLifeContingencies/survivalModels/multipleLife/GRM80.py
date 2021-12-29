from soa_tables import read_soa_table_xml as rst
from essential_life import mortality_table, commutation_table

table_names = ['TV7377', 'GRF95', 'GRM95', 'GRM80']
mt_lst = [rst.SoaTable('../../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=4, g=0, mt=mt.table_qx) for mt in mt_lst]

lt = lt_lst[-1]

'''
\px[3]{\overline{25:26}}
'''
p1 = lt.tpx(x=25, t=3)
p2 = lt.tpx(x=26, t=3)
p = p1 + p2 - p1 * p2

print(f'p1=', p1, f'p2=', p2, f'p1 p2=', p1 * p2, f'p=', p)

'''
\px[3]{25:26}
'''

p1 = lt.tpx(x=25, t=3)
p2 = lt.tpx(x=26, t=3)
p = p1 * p2

print(f'p1=', p1, f'p2=', p2, f'p1 p2=', p1 * p2)

'''
\qx[15]{\overline{25:26}}
'''
p1 = lt.tqx(x=25, t=15)
p2 = lt.tqx(x=26, t=15)
p = p1 * p2

print(f'p1=', p1, f'p2=', p2, f'p1 p2=', p1 * p2)

'''
\qx[3|2]{\overline{20:23}}
'''
p1 = lt.tqx(x=20, t=3 + 2)
p2 = lt.tqx(x=23, t=3 + 2)
a = p1 * p2

p1_b = lt.tqx(x=20, t=3)
p2_b = lt.tqx(x=23, t=3)
b = p1_b * p2_b
h = a -b

print(f'p1=', p1, f'p2=', p2, f'p1_=', p1_b, f'p2=', p2_b, f'h=', h)
