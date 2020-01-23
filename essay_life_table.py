# author: PedroCR #
from mortality_tables_old import TV7377, GKM95, GKM95_15, GKM95_lx_15
import mortality_table
import commutation_table

lt_tv7377 = mortality_table.MortalityTable(mt=TV7377)
lt_gkm95 = mortality_table.MortalityTable(data_type='l', mt=GKM95_lx_15)

cf_tv7377 = commutation_table.CommutationFunctions(i=4, g=0, mt=TV7377)
print(cf_tv7377.df_commutation_table())

# test to probabilities
p = lt_gkm95.tpx(x=50, t=5)
q = lt_gkm95.tqx(x=50, t=5)
print(p)
print(q)
print(p + q)
print(lt_gkm95.msn)

print(lt_gkm95.lx_udd(25.5))
print(lt_gkm95.lx_cfm(25.5))
print(lt_gkm95.lx_bal(25.5))

print(lt_gkm95.t_nqx(x=25.5, t=5.2, n=2.3, method='cfm'))
print(lt_gkm95.msn)

print('Insurances')
print(cf_tv7377.nEx(30, 35), '=', cf_tv7377.msn[-1])
print(cf_tv7377.Ax(30), '=', cf_tv7377.msn[-1])
