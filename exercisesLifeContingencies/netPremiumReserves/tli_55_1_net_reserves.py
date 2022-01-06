from exercisesLifeContingencies.lifeInsurance import tli_55_1
import pandas as pd
import matplotlib.pyplot as plt

'''
Net premium reserves path
'''
reserves_dict = {'table': [], 'x': [], 'insurer': [], 'insured': [], 'reserve': []}
ages = range(tli_55_1.x, tli_55_1.x + tli_55_1.term + 1)
print('\n\n Net Premium reserves \n\n')
for idx_clt, clt in enumerate(tli_55_1.ct_lst):
    premium_unit = tli_55_1.tli[idx_clt]
    premium_capital = tli_55_1.capital * premium_unit
    premium_unit_leveled = premium_unit / tli_55_1.tad[idx_clt]
    premium_leveled = premium_unit_leveled * tli_55_1.capital
    for age in ages:
        reserves_dict['table'].append(tli_55_1.table_names[idx_clt])
        reserves_dict['x'].append(age)
        insurer_liability = clt.nAx(x=age, n=tli_55_1.term - (age - tli_55_1.x)) * tli_55_1.capital
        reserves_dict['insurer'].append(insurer_liability)
        insured_liability = premium_leveled * clt.naax(x=age, n=tli_55_1.term_annuity - (age - tli_55_1.x))
        reserves_dict['insured'].append(insured_liability)
        reserve = insurer_liability - insured_liability
        reserves_dict['reserve'].append(reserve)

reserves_df = pd.DataFrame(reserves_dict)

name = 'tli_55_1'
reserves_df.to_excel(excel_writer=name + '_netReserves' + '.xlsx', sheet_name=name,
                     index=False, freeze_panes=(1, 1))

'''
plot the reserves
'''
for idx_clt, clt in enumerate(tli_55_1.ct_lst):
    plt.plot(ages, reserves_df.loc[reserves_df['table'] == tli_55_1.table_names[idx_clt]]['reserve'],
             label=tli_55_1.table_names[idx_clt])

plt.xlabel(r'$x$')
plt.ylabel('Reserves')
plt.title('Net Premium Reserves Term Life Insurance')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
# plt.savefig(this_py + '.eps', format='eps', dpi=3600)
plt.show()
