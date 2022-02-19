import reinsurance_types as rt
import numpy as np
import matplotlib.pyplot as plt

qs = rt.QuotaShare(cedant_share=0.1, total_capacity=1E7, capital_at_risk=0)
sp = rt.Surplus(cedant_line=1E6, total_capacity=1E7, capital_at_risk=0)

capital_at_risk = np.linspace(0, 1E7, 1001)
sp_cedant_share = []
sp_reinsurance_share = []

for j in capital_at_risk:
    sp.capital_at_risk = j
    sp_cedant_share.append(sp.cedant_share)
    sp_reinsurance_share.append(1 - sp.cedant_share)

fig, axes = plt.subplots()
plt.plot(capital_at_risk, sp_cedant_share, label='Cedant share in Surplus')
plt.plot(capital_at_risk, sp_reinsurance_share, label='Reinsurer share in Surplus')
plt.grid(visible=True, which='both', axis='both', color='grey', linestyle='-', linewidth=.1)
plt.axhline(y=qs.cedant_share, xmin=0.05, color='r', linestyle='-', label='Quota-share')
plt.xlabel('capital@risk')
plt.ylabel('share in %')
plt.title('Quota-Share versus Surplus')
plt.legend()
plt.show()
