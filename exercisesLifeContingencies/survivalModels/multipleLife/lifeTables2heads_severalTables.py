import numpy as np
import os
import sys

from soa_tables import read_soa_table_xml as rst
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


dif_age = 3
l0 = 100000

table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]

lt_q_min_xy = []
lt_q_max_xy = []

for lt in lt_lst:
    l = [1 - lt.tpx(x=x, t=1) * lt.tpx(x=x + dif_age, t=1) for x in range(lt.w - dif_age + 1)]
    l.insert(0, 0)
    lt_q_min_xy.append(l)
    l = [lt.tqx(x=x, t=1) * lt.tqx(x=x + dif_age, t=1) for x in range(lt.w - dif_age + 1)]
    l.insert(0, 0)
    lt_q_max_xy.append(l)

lt_min_lxy_lst = [mortality_table.MortalityTable(mt=mt) for mt in lt_q_min_xy]
lt_max_lxy_lst = [mortality_table.MortalityTable(mt=mt) for mt in lt_q_max_xy]
