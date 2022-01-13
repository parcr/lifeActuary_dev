'''
\item
Considering \textbf{Makehams law of mortality} with $A=0.0004,B=1.2E-6$ and $c=1.08$ with a rate of interest of $1.8\%$/annum, determine:

\begin{enumerate}
\item The 5 years monthly leveled risk premiums for an Endowment Insurance with term 10 years purchased by a life aged 50 if the payment in the event of death happens at the final of quarter of the death with capital underwritten $100\:000$\euro.

\item The 15 years leveled risk premiums for a Whole Life Insurance purchased by a life aged 50, paying $200\:000$\euro\ at the moment of death.

\item What is price for the single premium (risk single premium) of the guarantee if a life 65 years old decide to swap a whole life annuity-due that pays $10\:000$\euro$\:$ per year for an annuity with a guarantee of $10$ terms.
\end{enumerate}
'''

import pandas as pd
from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]
mml = makeham_mortality_functions.Makeham(a=0.0004, b=1.2E-6, c=1.08)

e0 = mml.moments_Tx()
print('e0=', e0)

w = 125
interest_rate = 1.8
interest_rate_2 = ((1 + interest_rate / 100) ** 2 - 1) * 100

'''
Compute Life Table
'''
px = np.array([mml.S(x, t=1) for x in range(0, w)])
qx = 1 - px
lt = mortality_table.MortalityTable(mt=list(np.append(0, qx)))
lt.df_life_table().to_excel(excel_writer='makeham' + '.xlsx', sheet_name='makeham',
                            index=False, freeze_panes=(1, 1))
ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=list(np.append(0, qx)))
ct.df_commutation_table().to_excel(excel_writer='makeham_comm' + '.xlsx', sheet_name='makeham',
                                   index=False, freeze_panes=(1, 1))
ct_2 = commutation_table.CommutationFunctions(i=interest_rate_2, g=0, mt=list(np.append(0, qx)))

'''
\item The 5 years monthly leveled risk premiums for an Endowment Insurance with term 10 years purchased by a life aged 
50 if the payment in the event of death happens at the final of quarter of the death with capital 
underwritten $100\:000$\euro.
'''
capital_endowment = 100000
x = 50
term = 10
term_annuity = 5


