'''
\item Consider a life aged 45 that buys a 20 years Pure Endowment Insurance at an interest rate of $1.25\%$/year and capital $100\:000$\euro.


\begin{enumerate}
\item Determine the cost of refunding the 10 years leveled premiums.

\item Determine the net risk premium if the Pure Endowment cover is swapped by an Endowment, with the capital in case of death paid at the end of the year of death and equal to $h\times 5\:000$\euro, where $h=1,..., 20$ is the period of death.
\end{enumerate}
'''

import numpy as np

from soa_tables import read_soa_table_xml as rst
from essential_life import mortality_table, commutation_table

table_names = ['TV7377', 'GRF95', 'GRM95']
interest_rate = 1.25
mt_lst = [rst.SoaTable('../../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
ct_lst = [commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=mt.table_qx) for mt in mt_lst]

table_index = 0  # unisex

x = 45
term = 20
term_annuity = 10
capital = 100000

print('\nq1')
print('Leveled Net Risk Premium Refund at End of the Year of Death')
pureEndow = ct_lst[table_index].nEx(x=x, n=term)
tad = ct_lst[table_index].naax(x=x, n=term_annuity, m=1)
tli_increasing = ct_lst[table_index].nIAx(x=x, n=term_annuity)
tli_deferred = ct_lst[table_index].t_nAx(x=x, n=term - term_annuity, defer=term_annuity)
pureEndow_leveled_refund = pureEndow / (tad - tli_increasing - term_annuity * tli_deferred)

print('pureEndow:', round(pureEndow, 10))
print('tad:', round(tad, 10))
print('tli_increasing:', round(tli_increasing, 10))
print('tli_deferred:', round(tli_deferred, 10))
print('pureEndow_leveled_refund:', round(pureEndow_leveled_refund, 10))
print('pureEndow_leveled_refund_capital:', round(capital * pureEndow_leveled_refund, 5))
