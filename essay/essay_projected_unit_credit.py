__author__ = "PedroCR"

from soa_tables import read_soa_table_xml as rst
from disability_tables import disability_tables as dt
from turnover_tables import turnover_tables as tt
import mortality_table as mt
from multidecrement_table import MultiDecrementTable as mdt
import age
from amortization_schemes.projected_unit_credit import puc

soa_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
ekv80 = dt.EVK_80
ekv80_70 = dt.EVK_80_ext_70
pcr1 = tt.pcr_turnover
pcr2 = tt.pcr_turnover_65

mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)
dt_ekv80 = mt.MortalityTable(mt=ekv80, last_q=0)
# dt_ekv80.force_qw_0()
tt_pcr = mt.MortalityTable(mt=pcr1, last_q=0)
# tt_pcr.force_qw_0()

tables_unidecrement = {'mortality': mt_TV7377, 'disability': dt_ekv80, 'turnover': tt_pcr}

tables_multidecrement = mdt(dict_tables=tables_unidecrement)
tables_multidecrement.create_udd_multidecrement_table()

dict_dates = {'date_of_birth': '1977-03-12', 'date_of_entry': '1997-05-15'}
date_of_valuation = '2019-12-31'
dict_ages = dict()
for k_d, v_d in dict_dates.items():
    new_age = age.Age(date1=v_d, date2=date_of_valuation)
    dict_ages[k_d.replace('date_of', 'age_at')] = new_age.age_act()

age_cost = age.Age(date1=dict_dates['date_of_entry'], date2=dict_dates['date_of_entry']).date_inc_years(40)
age_cost_2 = age.Age(date1=dict_dates['date_of_birth'], date2=dict_dates['date_of_birth']).date_inc_years(55)

print(dict_ages)
print('date_at_term_cost:', age_cost.date2, 'or', age_cost_2.date2)
max_date = min(age_cost.date2, age_cost_2.date2)
print('the oldest date is:', max_date)

# PUC
print('\n')
pUC = puc.PUC(date_of_valuation=date_of_valuation, date_of_birth=dict_dates['date_of_birth'],
              date_of_entry=dict_dates['date_of_entry'], date_of_term_cost=str(max_date),
              multi_table=tables_multidecrement, decrement=1, i=2, waiting_first_instalment=None,
              waiting_last_instalment=None, waiting_first_payment=None)

pUC.set_default_waiting_periods()

# compute pvfb
x = 45
print(f"PVBT({pUC.y}, {pUC.x}, {pUC.z}|{x})={pUC.pvfb(x=x)}")
print(f"PVBT({pUC.y}, {pUC.x}, {pUC.z}|{pUC.x})={pUC.pvfb_x()}")
