import numpy as np
import os
import sys
from soa_tables import read_soa_table_xml as rst
from essential_life import mortality_table, commutation_table

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../../../soa_tables/' + name + '.xml') for name in table_names]
mux_udd = [np.array(t.table_qx[1:]) / (1 - np.array(t.table_qx[1:])) for t in mt_lst]
mux_cfm = [-np.log(1 - np.array(t.table_qx[1:])) for t in mt_lst]

alpha = 0.95
beta = 0.001
qx_changed = [list(1 - (1 - np.array(t.table_qx[1:])) ** alpha * np.exp(-beta)) for idx_t, t in enumerate(mt_lst)]
[qx_changed[idx_t].insert(0, mt_lst[idx_t].table_qx[0]) for idx_t, t in enumerate(mt_lst)]
for idx_t, t in enumerate(qx_changed):
    first_age = mt_lst[idx_t].table_qx[0]
    qx_changed[idx_t].insert(0, first_age)
