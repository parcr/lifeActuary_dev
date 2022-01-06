from exercisesLifeContingencies.lifeInsurance import wli_55_1
import pandas as pd
import matplotlib.pyplot as plt

'''
Net premium reserves path
'''
reserves_dict = {'table': [], 'x': [], 'insurer': [], 'insured': [], 'reserve': []}
w_s = [lt.w + 1 for lt in wli_55_1.lt_lst]  # all age limits for each table
max_w = max(w_s)
ages = range(wli_55_1.x, max_w)
print('\n\n Net Premium reserves \n\n')
for idx_clt, clt in enumerate(wli_55_1.ct_lst):
    premium_unit = wli_55_1.wli[idx_clt]
    premium_capital = wli_55_1.capital * premium_unit
    premium_unit_leveled = premium_unit / wli_55_1.tad[idx_clt]
    premium_leveled = premium_unit_leveled * wli_55_1.capital
    for age in ages:
        reserves_dict['table'].append(wli_55_1.table_names[idx_clt])
        reserves_dict['x'].append(age)
        insurer_liability = clt.Ax(x=age) * wli_55_1.capital
        reserves_dict['insurer'].append(insurer_liability)
        if wli_55_1.term - (age - wli_55_1.x) > 0:
            insured_liability = premium_leveled * clt.naax(x=age, n=wli_55_1.term - (age - wli_55_1.x))
        else:
            insured_liability = 0
        reserves_dict['insured'].append(insured_liability)
        reserve = insurer_liability - insured_liability
        reserves_dict['reserve'].append(reserve)

reserves_df = pd.DataFrame(reserves_dict)
name = 'wli_55_1'
reserves_df.to_excel(excel_writer=name + '_netReserves' + '.xlsx', sheet_name=name,
                     index=False, freeze_panes=(1, 1))

'''
plot the reserves
'''
for idx_clt, clt in enumerate(wli_55_1.ct_lst):
    plt.plot(ages, reserves_df.loc[reserves_df['table'] == wli_55_1.table_names[idx_clt]]['reserve'],
             label=wli_55_1.table_names[idx_clt])

plt.xlabel(r'$x$')
plt.ylabel('Reserves')
plt.title('Net Premium Reserves Endowment')
plt.grid(b=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
# plt.savefig(this_py + '.eps', format='eps', dpi=3600)
plt.show()
