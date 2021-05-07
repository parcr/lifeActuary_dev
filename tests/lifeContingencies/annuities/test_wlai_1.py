import pytest

from soa_tables import read_soa_table_xml as rst
from essential_life import mortality_table, commutation_table

table_names = ['TV7377', 'GRF95', 'GRM95']
mt_lst = [rst.SoaTable('../../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=4, g=0, mt=mt.table_qx) for mt in mt_lst]


def test_wlai_1():
    a = ct_lst[0].ax(x=55, m=1)
    assert 14.979275670997 == pytest.approx(a, rel=1e-12)


def test_wlai_2():
    a = ct_lst[1].ax(x=55, m=1)
    assert 18.019955773856 == pytest.approx(a, rel=1e-12)


def test_wlai_3():
    a = ct_lst[2].ax(x=55, m=1)
    assert 15.531276786555 == pytest.approx(a, rel=1e-12)