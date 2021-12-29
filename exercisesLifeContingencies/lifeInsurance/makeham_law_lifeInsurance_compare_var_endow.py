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
term = 10
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
Ax_comm = [ct.nAx(x=x, n=10) for x in ages]
Ax_2_comm = [ct_2.nAx(x, n=10) for x in ages]
Ex_comm = [ct.nEx(x=x, n=10) for x in ages]
Ex_2_comm = [ct_2.nEx(x, n=10) for x in ages]
AEx_comm = [Ax_comm[j] * capital + Ex_comm[j] * capital for j in range(len(ages))]
AEx_comm_compare = [ct.nAEx(x=x, n=10) * capital for x in ages]
AEx_comm_error = (np.array(AEx_comm) - np.array(AEx_comm_compare))

Ax_comm_var = [Ax_2_comm[j] - np.power(Ax_comm[j], 2) for j in range(len(ages))]
Ex_comm_var = [Ex_2_comm[j] - np.power(Ex_comm[j], 2) for j in range(len(ages))]
Ax_Ex_comm_cov = [Ax_comm[j] * Ex_comm[j] for j in range(len(ages))]
AEx_comm_std_dev = [np.sqrt(Ax_comm_var[j] + Ex_comm_var[j] - 2 * Ax_Ex_comm_cov[j]) * capital for j in
                    range(len(ages))]

'''
compute Whole Life Insurance with fraction for fraction ages using the survival function to compute 
the probabilities of non integer ages
'''
# todo: needs to be dapted for the endowment
Ax_4 = [mml.life_insurance(x=x, interest_rate=interest_rate, age_first_instalment=x, terms=term, fraction=4, w=129)
        for x in ages]
Ax_2_4 = [
    mml.life_insurance(x=x, interest_rate=interest_rate_2, age_first_instalment=x, terms=term, fraction=4, w=129)
    for x in ages]
Ax_4_var = [Ax_2_4[j] - np.power(Ax_4[j], 2) for j in range(len(ages))]
AEx_4 = [Ax_4[j] * capital + Ex_comm[j] * capital for j in range(len(ages))]
Ax_Ex_4_cov = [Ax_4[j] * Ex_comm[j] for j in range(len(ages))]
AEx_4_std_dev = [np.sqrt(Ax_4_var[j] + Ex_comm_var[j] - 2 * Ax_Ex_4_cov[j]) * capital for j in
                 range(len(ages))]




Ax_12 = [mml.life_insurance(x=x, interest_rate=interest_rate, age_first_instalment=x, terms=term, fraction=12, w=129)
         for x in ages]
Ax_2_12 = [
    mml.life_insurance(x=x, interest_rate=interest_rate_2, age_first_instalment=x, terms=term, fraction=12, w=129)
    for x in ages]
Ax_12_var = [Ax_2_12[j] - np.power(Ax_12[j], 2) for j in range(len(ages))]
AEx_12 = [Ax_12[j] * capital + Ex_comm[j] * capital for j in range(len(ages))]
Ax_Ex_12_cov = [Ax_12[j] * Ex_comm[j] for j in range(len(ages))]
AEx_12_std_dev = [np.sqrt(Ax_12_var[j] + Ex_comm_var[j] - 2 * Ax_Ex_12_cov[j]) * capital for j in
                  range(len(ages))]

'''
compute Whole Life Insurance for fraction ages using the survival function to compute 
the probabilities of non integer ages
'''

Ax_cont = [mml.Ax(x=x, interest_rate=interest_rate, n=term) for x in ages]
Ax_2_cont = [mml.Ax(x=x, interest_rate=interest_rate_2, n=term) for x in ages]
Ax_cont_var = [Ax_2_cont[j] - np.power(Ax_cont[j], 2) for j in range(len(ages))]
AEx_cont = [Ax_cont[j] * capital + Ex_comm[j] * capital for j in range(len(ages))]
Ax_Ex_cont_cov = [Ax_cont[j] * Ex_comm[j] for j in range(len(ages))]
AEx_cont_std_dev = [np.sqrt(Ax_cont_var[j] + Ex_comm_var[j] - 2 * Ax_Ex_cont_cov[j]) * capital for j in
                    range(len(ages))]

'''
compute Whole Life Insurance for fraction ages using the using Commutation Functions and the usual approximations
see formulas 4.27 and 4.28 from Actuarial Mathematics for Life Contingency Risks 
'''


def effective_nominal_interest_rate(interest_rate, freq):
    '''
    Convert effective interest rates to nominal interest rates
    :return:
    '''
    return (np.power(1 + interest_rate / 100., 1 / freq) - 1) * freq * 100


factor_1 = interest_rate / effective_nominal_interest_rate(interest_rate=interest_rate, freq=4)
factor_2 = interest_rate_2 / effective_nominal_interest_rate(interest_rate=interest_rate_2, freq=4)
Ax_comm_4 = np.array(Ax_comm) * factor_1
Ax_2_comm_4 = np.array(Ax_2_comm) * factor_2
Ax_comm_4_var = Ax_2_comm_4 - np.power(Ax_comm_4, 2)
AEx_comm_4 = [Ax_comm_4[j] * capital + Ex_comm[j] * capital for j in range(len(ages))]
Ax_Ex_comm_4_cov = [Ax_comm_4[j] * Ex_comm[j] for j in range(len(ages))]
AEx_comm_4_std_dev = [np.sqrt(Ax_comm_4_var[j] + Ex_comm_var[j] - 2 * Ax_Ex_comm_4_cov[j]) * capital for j in
                      range(len(ages))]

factor_1 = interest_rate / effective_nominal_interest_rate(interest_rate=interest_rate, freq=12)
factor_2 = interest_rate_2 / effective_nominal_interest_rate(interest_rate=interest_rate_2, freq=12)
Ax_comm_12 = np.array(Ax_comm) * factor_1
Ax_2_comm_12 = np.array(Ax_2_comm) * factor_2
Ax_comm_12_var = Ax_2_comm_12 - np.power(Ax_comm_12, 2)
AEx_comm_12 = [Ax_comm_12[j] * capital + Ex_comm[j] * capital for j in range(len(ages))]
Ax_Ex_comm_12_cov = [Ax_comm_12[j] * Ex_comm[j] for j in range(len(ages))]
AEx_comm_12_std_dev = [np.sqrt(Ax_comm_12_var[j] + Ex_comm_var[j] - 2 * Ax_Ex_comm_12_cov[j]) * capital for j in
                       range(len(ages))]

'''
Prepare the data frame
'''

rounded_to = 6
Ax_compare_df = pd.DataFrame({'Age': ages,
                              'AEx_comm': np.round(np.array(AEx_comm), rounded_to),
                              'AEx_comm_std_dev': np.round(AEx_comm_std_dev, rounded_to),
                              'AEx_4': np.round(np.array(AEx_4), rounded_to),
                              'AEx_4_std_dev': np.round(AEx_4_std_dev, rounded_to),
                              'AEx_12': np.round(np.array(AEx_12), rounded_to),
                              'AEx_12_std_dev': np.round(AEx_12_std_dev, rounded_to),
                              'AEx_cont': np.round(np.array(AEx_cont), rounded_to),
                              'AEx_cont_std_dev': np.round(AEx_cont_std_dev, rounded_to),
                              'AEx_comm_4': np.round(np.array(AEx_comm_4), rounded_to),
                              'AEx_comm_4_std_dev': np.round(AEx_comm_4_std_dev, rounded_to),
                              'AEx_comm_12': np.round(np.array(AEx_comm_12), rounded_to),
                              'AEx_comm_12_std_dev': np.round(AEx_comm_12_std_dev, rounded_to),
                              }
                             )
Ax_compare_df.to_excel(excel_writer='AEx_compare_temp_df' + '.xlsx', sheet_name='AEx_compare_temp',
                       index=False, freeze_panes=(1, 1))
