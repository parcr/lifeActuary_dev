import numpy as np
import pandas as pd
import os
import sys

from soa_tables import read_soa_table_xml as rst
from essential_life import mortality_table, commutation_table
import matplotlib.pyplot as plt

this_py = os.path.split(sys.argv[0])[-1][:-3]


def parse_table_name(name):
    return name.replace(' ', '').replace('/', '')


'''Reads the File'''
portfolio = pd.read_excel('portfolio_arm.xlsx')

''' Creates the Technical Basis of 1st and 2nd Order '''
table_names = ['GRM95', 'GRF95']
mt_lst = [rst.SoaTable('../soa_tables/' + name + '.xml') for name in table_names]
lt_lst = [mortality_table.MortalityTable(mt=mt.table_qx) for mt in mt_lst]
interest_rate_endow_1 = 2.1
interest_rate_endow_2 = 2.5
interest_rate_ann_1 = 1.3
interest_rate_ann_2 = 1.5

ct_lst_endow_1 = [commutation_table.CommutationFunctions(i=interest_rate_endow_1,
                                                         g=0, mt=mt.table_qx) for mt in mt_lst]
ct_lst_endow_2 = [commutation_table.CommutationFunctions(i=interest_rate_endow_2,
                                                         g=0, mt=mt.table_qx) for mt in mt_lst]
ct_lst_ann_1 = [commutation_table.CommutationFunctions(i=interest_rate_ann_1,
                                                       g=0, mt=mt.table_qx) for mt in mt_lst]
ct_lst_ann_2 = [commutation_table.CommutationFunctions(i=interest_rate_ann_2,
                                                       g=0, mt=mt.table_qx) for mt in mt_lst]

''' Starts Computing the Premiums at inception'''
premiums_endow_1 = []
annuity_endow_1 = []
premiums_endow_1_leveled = []
premiums_endow_2 = []
annuity_endow_2 = []
premiums_endow_2_leveled = []
pl_endowment = []

annuity_survival_1 = []
annuity_survival_2 = []
pl_annuity = []

age_final = 65

for index, row in portfolio.iterrows():
    if row['sex'] == 'm':
        index_table = 0
    else:
        index_table = 1

    # Premiums for Endowment
    premium_1 = ct_lst_endow_1[index_table].nAEx(x=row['age_0'], n=age_final - row['age_0']) * row['capital']
    annuity_1 = ct_lst_endow_1[index_table].naax(x=row['age_0'], n=row['#premiums'])
    premium_1_leveled = premium_1 / annuity_1

    premiums_endow_1.append(round(premium_1, 2))
    annuity_endow_1.append(round(annuity_1, 5))
    premiums_endow_1_leveled.append(round(premium_1_leveled, 2))

    premium_2 = ct_lst_endow_2[index_table].nAEx(x=row['age_0'], n=age_final - row['age_0']) * row['capital']
    annuity_2 = ct_lst_endow_2[index_table].naax(x=row['age_0'], n=row['#premiums'])
    premium_2_leveled = premium_2 / annuity_2

    premiums_endow_2.append(round(premium_2, 2))
    annuity_endow_2.append(round(annuity_2, 5))
    premiums_endow_2_leveled.append(round(premium_2_leveled, 2))

    # Premiums for Endowment...Expected Present value P&L
    pl_endow = (premium_1 - premium_2) * (1 + interest_rate_endow_2 / 100) ** (row['age'] - row['age_0'])
    pl_endowment.append(round(pl_endow, 2))

    # Premiums for Annuity
    annuity_1 = row['capital'] / ct_lst_ann_1[index_table].aax(x=age_final)
    annuity_2 = row['capital'] / ct_lst_ann_2[index_table].aax(x=age_final)

    annuity_survival_1.append(round(annuity_1, 2))
    annuity_survival_2.append(round(annuity_2, 2))

    # Premiums for Annuity...Expected Present value P&L
    pl_ann = ((ct_lst_ann_1[index_table].aax(x=age_final)/ct_lst_ann_2[index_table].aax(x=age_final)-1) *
              row['capital']) * (1 + interest_rate_endow_2 / 100) ** (row['age'] - age_final) * \
             ct_lst_ann_2[index_table].tpx(x=row['age'], t=age_final - row['age'])
    pl_annuity.append(round(pl_ann, 2))

portfolio['premiums_endow_1'] = premiums_endow_1
portfolio['annuity_endow_1'] = annuity_endow_1
portfolio['premiums_endow_1_leveled'] = premiums_endow_1_leveled

portfolio['premiums_endow_2'] = premiums_endow_2
portfolio['annuity_endow_2'] = annuity_endow_2
portfolio['premiums_endow_2_leveled'] = premiums_endow_2_leveled

portfolio["annuity_1"] = annuity_survival_1
portfolio["annuity_2"] = annuity_survival_2

portfolio['epv_endow'] = pl_endowment
portfolio['epv_annuity'] = pl_annuity

portfolio.index = np.arange(1, len(portfolio) + 1)

save_tables_boolean = False
if save_tables_boolean:
    portfolio.to_excel(excel_writer='portfolio_arm' + '_sol' + '.xlsx', sheet_name='sol',
                       index=True, index_label="policy", freeze_panes=(1, 1))

''' The Sums of P&L '''
sum_pl_endow = portfolio['epv_endow'].sum()
sum_pl_ann = portfolio['epv_annuity'].sum()
print('Expected Present Value P&L for Endowment:', "{:,.2f}".format(sum_pl_endow))
print('Expected Present Value P&L for Annuity:', "{:,.2f}".format(sum_pl_ann))
print('Expected Present Value P&L for the Product:', "{:,.2f}".format(sum_pl_endow + sum_pl_ann))
print('Expected Present Value P&L for the Product (50%):', "{:,.2f}".format(sum_pl_endow + sum_pl_ann / 2))

''' Some Statistics of the Portfolio '''
pd.set_option('display.max_columns', 500)
print()
print(portfolio.describe(include='all'))
