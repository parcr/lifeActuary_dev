import pandas as pd
from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]
mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)

# e0 = mml.moments_Tx()
ages = np.arange(start=20, stop=100 + 20, step=20)

interest_rate = 5
interest_rate_2 = ((1 + interest_rate / 100) ** 2 - 1) * 100
capital = 100000

'''
Compute Life Table
'''
interest_rate = 5
px = np.array([mml.S(x, t=1) for x in range(0, 128 + 1)])
qx = 1 - px
lt = mortality_table.MortalityTable(mt=list(np.append(0, qx)))
lt.df_life_table().to_excel(excel_writer='makeham' + '.xlsx', sheet_name='makeham',
                            index=False, freeze_panes=(1, 1))
ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=list(np.append(0, qx)))
ct_2 = commutation_table.CommutationFunctions(i=interest_rate_2, g=0, mt=list(np.append(0, qx)))

'''
compute Whole Life Insurance using Commutation Functions
'''
Ax_comm = [ct.Ax(x) for x in ages]
Ax_2_comm = [ct_2.Ax(x) for x in ages]
Ax_comm_std_dev = [np.power(Ax_2_comm[j] - np.power(Ax_comm[j], 2), .5) * capital for j in range(len(ages))]

'''
compute Whole Life Insurance with fraction for fraction ages using the survival function to compute 
the probabilities of non integer ages
'''
Ax_12 = [mml.life_insurance(x=x, interest_rate=interest_rate, age_first_instalment=x, terms=np.inf, fraction=12, w=129)
         for x in ages]
Ax_2_12 = [
    mml.life_insurance(x=x, interest_rate=interest_rate_2, age_first_instalment=x, terms=np.inf, fraction=12, w=129)
    for x in ages]
Ax_12_std_dev = [np.power(Ax_2_12[j] - np.power(Ax_12[j], 2), .5) * capital for j in range(len(ages))]

'''
compute Whole Life Insurance for fraction ages using the survival function to compute 
the probabilities of non integer ages
'''

Ax_cont = [mml.Ax(x=x, interest_rate=interest_rate, n=np.inf) for x in ages]
Ax_2_cont = [mml.Ax(x=x, interest_rate=interest_rate_2, n=np.inf) for x in ages]
Ax_cont_std_dev = [np.power(Ax_2_cont[j] - np.power(Ax_cont[j], 2), .5) * capital for j in range(len(ages))]

Ax_compare_df = pd.DataFrame({'Age': ages,
                              'Ax_comm': np.round(np.array(Ax_comm) * capital, 2),
                              'Ax_comm_std_dev': np.round(Ax_comm_std_dev, 2),
                              'Ax_12': np.round(np.array(Ax_12) * capital, 2),
                              'Ax_12_std_dev': np.round(Ax_12_std_dev, 2),
                              'Ax_cont': np.round(np.array(Ax_cont) * capital, 2),
                              'Ax_cont_std_dev': np.round(Ax_cont_std_dev, 2)}, )
Ax_compare_df.to_excel(excel_writer='Ax_compare_df' + '.xlsx', sheet_name='Ax_compare',
                       index=False, freeze_panes=(1, 1))
