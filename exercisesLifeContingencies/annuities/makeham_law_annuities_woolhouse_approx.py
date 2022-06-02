from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
import numpy as np
from essential_life import mortality_table, commutation_table
import pandas as pd
import os
import sys

this_py = os.path.split(sys.argv[0])[-1][:-3]
mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)


'''
Compute Life Table and commutation table
'''
period = 10
x_s = list(range(20, 100 + 10, 10))
interest_rate = 10
px = np.array([mml.S(x, t=1) for x in range(0, 130 + 1)])
qx = 1 - px
lt = mortality_table.MortalityTable(mt=list(np.append(0, qx)))
ct = commutation_table.CommutationFunctions(i=interest_rate, g=0, mt=list(np.append(0, qx)))

'''
annuities temp
'''
rendas_temp_dict = {'x': list(), "type": list(), 'Exact': list(), 'Continuous': list(),
                    'UDD': list(), 'W2': list(),
                    'W3': list(), 'W3_app': list()}

for x in x_s:
    for m in [12]:
        # ts = np.arange(0, period + 1 / m, 1 / m) # todo: it is inconsistent, be careful
        ts = np.linspace(start=0, stop=period, num=m * period + 1, endpoint=True)
        i = interest_rate / 100
        v = 1 / (1 + i)
        # exact
        rendas_temp_dict['x'].append(x)
        epv_ai = [mml.S(x=x, t=u) * np.power(v, u) for u in ts[1:]]
        epv_aa = epv_ai.copy()
        epv_aa.insert(0, 1)
        epv_aa.pop()
        rendas_temp_dict['type'].append('aa_' + str(x) + '_' + str(m))
        rendas_temp_dict['Exact'].append(sum(epv_aa) / m)
        # rendas_temp_dict['type'] = 'ai_' + str(x) + '_' + str(m)
        # rendas_temp_dict['Exact'] = sum(epv_ai) / m
        # continuous
        rendas_temp_dict['Continuous'].append(mml.ax(x=x, interest_rate=interest_rate, n=period)[0])

        # commutation table
        d = i * v
        i_m = (np.power((1 + i), 1 / m) - 1) * m
        d_m = i_m * np.power((1 + i), -1 / m)
        alpha_m = i * d / (i_m * d_m)
        beta_m = (i - i_m) / (i_m * d_m)
        delta = np.log(1 + i)
        rendas_temp_dict['W2'].append(ct.naax(x=x, n=period, m=m))  # Woolhouse 2 terms
        rendas_temp_dict['UDD'].append(ct.naax(x=x, n=period, m=1) * alpha_m - beta_m * (1 - ct.nEx(x=x, n=period)))
        # rendas_temp_dict['UDD_app'] = ct.nax(x=x, n=period, m=m)
        # rendas_temp_dict['UDD'] = ct.nax(x=x, n=period, m=1) * alpha_m - (-alpha_m + beta_m + 1 / m) * \
        #                          (1 - ct.nEx(x=x, n=period))

        # Woolhouse 3 terms
        renda = sum([mml.S(x=x, t=u) * v ** u for u in range(0, period)])
        factor1 = (m - 1) / (2 * m) * (1 - ct.nEx(x, period))
        factor2 = (m ** 2 - 1) / (12 * m ** 2) * (delta + mml.mu(x) - ct.nEx(x, period) * (delta + mml.mu(x + period)))
        rendas_temp_dict['W3'].append(renda - factor1 - factor2)
        mu_x_app = -.5 * np.log(ct.npx(x=x - 1, n=2))
        mu_x_n_app = -.5 * np.log(ct.npx(x=x - 1 + period, n=2))
        factor2_app = (m ** 2 - 1) / (12 * m ** 2) * (
                delta + mu_x_app - ct.nEx(x, period) * (delta + mu_x_n_app))
        rendas_temp_dict['W3_app'].append(renda - factor1 - factor2_app)

df = pd.DataFrame(rendas_temp_dict)
df.to_excel(this_py + '_' + str(interest_rate) + '.xlsx', index=False, freeze_panes=(1, 0))
