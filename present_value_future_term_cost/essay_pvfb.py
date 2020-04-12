__author__ = "PedroCR"

from soa_tables import read_soa_table_xml as rst
from disability_tables import disability_tables as dt
from turnover_tables import turnover_tables as tt
import mortality_table as mt
from multidecrement_table import MultiDecrementTable as mdt
import age
from present_value_future_term_cost import pvftc
from matplotlib import pyplot as plt

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

dict_dates = {'date_of_birth': '1977-03-12', 'date_of_entry': '1997-05-15'}
date_of_valuation = '2019-12-31'

dates_for_term_cost = age.Age(date1=dict_dates['date_of_birth'], date2=dict_dates['date_of_birth']).date_inc_years(55)
age_term_cost_years = dates_for_term_cost.age_act()
pvfb_d = pvftc.PVTermCost(date_of_valuation=date_of_valuation, date_of_birth=dict_dates['date_of_birth'],
                          date_of_entry=dict_dates['date_of_entry'], age_of_term_cost=age_term_cost_years,
                          waiting=0,
                          multi_table=tables_multidecrement, decrement='disability', i=2, age_of_projection=None)

pvfb_d.age_of_projection = pvfb_d.x
print(pvfb_d.profile)
pvfb_d.waiting = 1
print(pvfb_d.profile)
pvfb_d.age_of_term_cost = 60
print(pvfb_d.profile)

'''

'''

'''We get all the pv for all term costs for disability'''
print('\nPVFTC\n')
pvfb_d.waiting = 0
pvfb_d.age_of_term_cost = 55
x = pvfb_d.y
pvtc = pvfb_d.pvftc_proj(x=x, px=x)
print(pvtc)
x = pvfb_d.x
pvtc = pvfb_d.pvftc_proj(x=x, px=x)
print(pvtc)
x = pvfb_d.x + 3
pvtc = pvfb_d.pvftc_proj(x=x, px=x)
print(pvtc)
x = pvfb_d.age_of_term_cost - 1
pvtc = pvfb_d.pvftc_proj(x=x, px=x)
print(pvtc)
x = pvfb_d.age_of_term_cost
pvtc = pvfb_d.pvftc_proj(x=x, px=x)
print(pvtc)
x = pvfb_d.age_of_term_cost + 1
pvtc = pvfb_d.pvftc_proj(x=x, px=x)
print(pvtc)
x = pvfb_d.age_of_term_cost + 5
pvtc = pvfb_d.pvftc_proj(x=x, px=x)
print(pvtc)
'''



'''
print('\nSums\n')
x = pvfb_d.y
lst_pvftc = pvfb_d.lst_pvftc(age_first_term_cost=pvfb_d.y + 1, age_last_term_cost=65)
print(lst_pvftc)
