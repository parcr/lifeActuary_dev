'''
Considering \textbf{Makehams law of mortality} with $A=0.0004,B=1.2E-6$ and $c=1.08$ with a rate of interest of $1.8\%$/annum, determine:

\begin{enumerate}
\item The 5 years monthly leveled risk premiums for an Endowment Insurance with term 10 years purchased by a life aged 50 if the payment in the event of death happens at the final of quarter of the death with capital underwritten $100\:000$\euro.

\item The 15 years leveled risk premiums for a Whole Life Insurance purchased by a life aged 50, paying $200\:000$\euro\ at the moment of death.

\item What is the reduction produced by the guarantee of $10$ terms, if a life 65 years old decide to swap a whole life annuity-due that pays $10\:000$\euro$\:$ per year for an annuity with this guarantee.
'''

import numpy as np
from annuities_certain import annuities_certain
import pandas as pd
import os
import sys

from soa_tables import read_soa_table_xml as rst
from essential_life import mortality_table, commutation_table

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 2
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]
# ages = np.linspace(start=20, stop=40, num=5, dtype=int)

table_index = 1  # woman
'''
\item For a capital of $500\:000$\euro, the monthly leveled risk premiums paid 25 years if in case of death 
the capital is paid at the moment of death.
'''

x = 30
term = 35
annuity_terms = 25
annuity_fraction = 12
capital = 500000

tad_1 = ct_lst[table_index].naax(x=x, n=annuity_terms, m=1)
tad_12 = ct_lst[table_index].naax(x=x, n=annuity_terms, m=annuity_fraction)
endowment_ = ct_lst[table_index].nAEx_(x=x, n=term)
pure_endowment = ct_lst[table_index].nEx(x=x, n=term)
tli_ = ct_lst[table_index].nAx_(x=x, n=term)
single_premium_capital = endowment_ * capital
leveled_premium_capital = single_premium_capital / tad_12 / annuity_fraction

print('\n q1')
print('term life insurance_:', round(tli_, 10))
print('pure_endowment:', round(pure_endowment, 10))
print('single_premium_unit:', round(endowment_, 10))
print('test:', (tli_ + pure_endowment) - endowment_)
print('single_premium_capital:', round(single_premium_capital, 5))
print('tad_12:', round(tad_12, 10))
print('leveled_premium_capital:', round(leveled_premium_capital, 5))

'''\item The 15 years leveled risk premiums for a Whole Life Insurance purchased by a life aged 50, paying 
$200\:000$\euro\ at the moment of death.
'''
print('\n q2')
endow = ct_lst[table_index].nAEx(x=x, n=term)
v = 1 / (1 + interest_rate / 100)
support = [v ** j for j in range(1, term + 1)]
pmf = [ct_lst[table_index].t_nqx(x=x, t=j - 1, n=1) for j in range(1, term)]
pmf.append(ct_lst[table_index].tpx(x=x, t=term - 1))
cdf = np.cumsum(pmf)

print('endowment:', round(endow, 10))
print('support', support)
print('pmf:', pmf)
print('cdf', cdf)
epv_lst = [pmf[j] * support[j] for j in range(0, term)]
print('expected present value:', sum(epv_lst))
print('test:', sum(epv_lst) - endow)
cut_year = np.log(endow) / np.log(v)
print('cut_year:', cut_year)
print('cut_probability:', round(ct_lst[table_index].tpx(x=x, t=term - 1), 10))
print('answer:', round(1 - ct_lst[table_index].tpx(x=x, t=term - 1), 10) * 100, '%', sep='')

# another way
probs_bool = [pmf[idx_v] for idx_v, v in enumerate(support) if v > endow]
print('answer:', round(sum(probs_bool), 10) * 100, '%', sep='')

'''
\item For a capital of $500\:000$\euro, the single risk premium if in case of death the capital is paid at the 
end of the year but considering that the cover is deferred until the age of 40, keeping the term age at 65.
'''

print('\n q3')
defer = 5
term = term - defer
deferment_factor = ct_lst[table_index].nEx(x=x, n=defer)
pure_endowment = ct_lst[table_index].nEx(x=x + defer, n=term)
term_life_insurance_ = ct_lst[table_index].nAx_(x=x + defer, n=term)
term_life_insurance = ct_lst[table_index].nAx(x=x + defer, n=term)
endowment = ct_lst[table_index].t_nAEx(x=x, n=term, defer=defer)

print(f'{table_names[table_index]} deferment_factor: {deferment_factor}')
print(f'{table_names[table_index]} term_life_insurance: {term_life_insurance}')
print(f'{table_names[table_index]} term_life_insurance_: {term_life_insurance_}')
print(f'{table_names[table_index]} pure_endowment: {pure_endowment}')
print(f'{table_names[table_index]} endowment: {endowment}')
print(f'{table_names[table_index]}: {endowment * capital}')
print('test=', deferment_factor * (term_life_insurance + pure_endowment) - endowment)
print()
