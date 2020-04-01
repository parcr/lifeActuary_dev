__author__ = "PedroCR"

from soa_tables import read_soa_table_xml as rst
from disability_tables import disability_tables as dt
from turnover_tables import turnover_tables as tt
import mortality_table as mt
from multidecrement_table import MultiDecrementTable as mdt
import numpy as np

soa_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
ekv80 = dt.EVK_80
ekv80_70 = dt.EVK_80_ext_70
pcr1 = tt.pcr_turnover
pcr2 = tt.pcr_turnover_65

mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)
dt_ekv80 = mt.MortalityTable(mt=ekv80, last_q=0)
tt_pcr = mt.MortalityTable(mt=pcr1, last_q=0)

tables_unidecrement = {'mortality': mt_TV7377, 'disability': dt_ekv80, 'turnover': tt_pcr}

tables_multidecrement = mdt(dict_tables=tables_unidecrement)
tables_multidecrement.create_udd_multidecrement_table()

# create a transition matrix
transition_info = [[(tables_multidecrement.net_table, 'p'),
                    (tables_multidecrement.multidecrement_tables['disability'], 'q'),
                    (tables_multidecrement.multidecrement_tables['turnover'], 'q'),
                    (tables_multidecrement.multidecrement_tables['mortality'], 'q')]]
transition_info.append([0,
                        (tables_multidecrement.unidecrement_tables['mortality'], 'p'),
                        0,
                        (tables_multidecrement.unidecrement_tables['mortality'], 'q')])
transition_info.append([0,
                        0,
                        (tables_multidecrement.unidecrement_tables['mortality'], 'p'),
                        (tables_multidecrement.unidecrement_tables['mortality'], 'q')])
transition_info.append([0,
                        0,
                        0,
                        1])


def transition_matrix_1(transition_info, x):
    c = len(transition_info)
    r = len(transition_info[0])
    mat = np.zeros((c, r))
    for r_i, r in enumerate(transition_info):
        for c_i, c in enumerate(r):
            if type(transition_info[r_i][c_i]) == tuple:
                if transition_info[r_i][c_i][1] == 'p':
                    mat[r_i][c_i] = transition_info[r_i][c_i][0].tpx(x=1, t=1, method='udd')
                else:
                    mat[r_i][c_i] = transition_info[r_i][c_i][0].tqx(x=x, t=1, method='udd')
            else:
                mat[r_i][c_i] = transition_info[r_i][c_i]
    return mat


mat = transition_matrix_1(transition_info, x=45)
