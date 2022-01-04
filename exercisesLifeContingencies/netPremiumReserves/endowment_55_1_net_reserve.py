from exercisesLifeContingencies.lifeInsurance import endowment_55_1
import pandas as pd
import matplotlib.pyplot as plt

'''
Net premium reserves path
'''
reserves_dict = {'table': [], 'x': [], 'insurer': [], 'insured': [], 'reserve': []}
ages = range(endowment_55_1.x, endowment_55_1.x + endowment_55_1.term + 1)
print('\n\n Net Premium reserves \n\n')
for idx_clt, clt in enumerate(endowment_55_1.ct_lst):
    premium_unit = endowment_55_1.endow[idx_clt]
    premium_capital = endowment_55_1.capital * premium_unit
    premium_unit_leveled = premium_unit / endowment_55_1.tad[idx_clt]
    premium_leveled = premium_unit_leveled * endowment_55_1.capital
    for age in ages:
        reserves_dict['table'].append(endowment_55_1.table_names[idx_clt])
        reserves_dict['x'].append(age)
        insurer_liability = clt.nAEx(x=age, n=endowment_55_1.term - (age - endowment_55_1.x)) * \
                            endowment_55_1.capital
        reserves_dict['insurer'].append(insurer_liability)
        insured_liability = premium_leveled * clt.naax(x=age, n=endowment_55_1.term_annuity -
                                                                (age - endowment_55_1.x))
        reserves_dict['insured'].append(insured_liability)
        reserve = insurer_liability - insured_liability
        reserves_dict['reserve'].append(reserve)

reserves_df = pd.DataFrame(reserves_dict)

'''
plot the reserves
'''
for idx_clt, clt in enumerate(endowment_55_1.ct_lst):
    plt.plot(ages, reserves_df.loc[reserves_df['table'] == endowment_55_1.table_names[idx_clt]]['reserve'],
             label=endowment_55_1.table_names[idx_clt])

plt.xlabel(r'$x$')
plt.ylabel('Reserves')
plt.title('Net Premium Reserves Endowment')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
# plt.savefig(this_py + '.eps', format='eps', dpi=3600)
plt.show()