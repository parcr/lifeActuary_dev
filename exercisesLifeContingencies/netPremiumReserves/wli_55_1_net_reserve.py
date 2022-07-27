from exercisesLifeContingencies.lifeInsurance import wli_55_1
import pandas as pd
import matplotlib.pyplot as plt

'''
Net premium reserves path
'''
l0 = 1000
reserves_dict = {'table': [], 'x': [], 'insurer': [], 'insured': [], 'reserve': []}
fund_dict = {'lx': [], 'claim': [], 'premium': [], 'fund': []}
# expected reserves value, that is, considering the survivorship of the group
expected_reserve_dict = {'insurer_exp': [], 'insured_exp': [], 'reserve_exp': []}
w_s = [lt.w + 1 for lt in wli_55_1.lt_lst]  # all age limits for each table
max_w = max(w_s)+1
ages = range(wli_55_1.x, max_w)
print('\n\n Net Premium reserves \n\n')
for idx_clt, clt in enumerate(wli_55_1.ct_lst):
    premium_unit = wli_55_1.wli[idx_clt]
    premium_capital = wli_55_1.capital * premium_unit
    premium_unit_leveled = premium_unit / wli_55_1.tad[idx_clt]
    premium_leveled = premium_unit_leveled * wli_55_1.capital
    for age in ages:
        # reserves # reserves # reserves # reserves # reserves # reserves
        reserves_dict['table'].append(wli_55_1.table_names[idx_clt])
        reserves_dict['x'].append(age)
        insurer_liability = clt.Ax(x=age) * wli_55_1.capital
        reserves_dict['insurer'].append(insurer_liability)
        tad = clt.naax(x=age, n=wli_55_1.term_annuity - (age - wli_55_1.x))
        if wli_55_1.term_annuity - (age - wli_55_1.x) > 0:
            insured_liability = premium_leveled * tad
        else:
            insured_liability = 0
        reserves_dict['insured'].append(insured_liability)
        reserve = insurer_liability - insured_liability
        reserves_dict['reserve'].append(reserve)

        prob_survival = clt.npx(x=wli_55_1.x, n=age - wli_55_1.x)
        lx = l0 * prob_survival
        expected_reserve_dict['insurer_exp'].append(insurer_liability * lx)
        expected_reserve_dict['insured_exp'].append(insured_liability * lx)
        expected_reserve_dict['reserve_exp'].append(reserve * lx)

        # fund # fund # fund # fund # fund # fund # fund # fund
        fund_dict['lx'].append(lx)
        qx_1 = clt.nqx(x=age - 1, n=1)
        claim = 0
        if (age > wli_55_1.x):
            claim = l0 * clt.npx(x=wli_55_1.x, n=age - wli_55_1.x - 1) * qx_1 * wli_55_1.capital
        fund_dict['claim'].append(claim)
        premium = 0
        if wli_55_1.term_annuity - (age - wli_55_1.x) > 0:
            premium = premium_leveled * lx
        fund_dict['premium'].append(premium)
        if age == wli_55_1.x:
            fund = lx * premium_leveled
        else:
            fund = fund_dict['fund'][-1] * (1 + wli_55_1.interest_rate / 100) - claim + premium
        fund_dict['fund'].append(fund)

reserves_df = pd.DataFrame(reserves_dict)
expected_reserve_df = pd.DataFrame(expected_reserve_dict)
fund_df = pd.DataFrame(fund_dict)
name = 'wli_55_1'
reserves_df.to_excel(excel_writer=name + '_netReserves' + '.xlsx', sheet_name=name, index=False, freeze_panes=(1, 1))

'''
plot the reserves
'''
for idx_clt, clt in enumerate(wli_55_1.ct_lst):
    plt.plot(ages, reserves_df.loc[reserves_df['table'] == wli_55_1.table_names[idx_clt]]['reserve'],
             label=wli_55_1.table_names[idx_clt])

plt.xlabel(r'$x$')
plt.ylabel('Reserves')
plt.title('Net Premium Reserves Endowment')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.legend()
# plt.savefig(this_py + '.eps', format='eps', dpi=3600)
plt.show()
