# author: PedroCR #
from toDelete.mortality_tables_old import TV7377, GKM95_lx_15
from essential_life import mortality_table, commutation_table

lt_tv7377 = mortality_table.MortalityTable(mt=TV7377)
lt_gkm95 = mortality_table.MortalityTable(data_type='l', mt=GKM95_lx_15)

cf_tv7377 = commutation_table.CommutationFunctions(i=2, g=1.5, mt=TV7377)
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
print(cf_tv7377.nEx(30, 350))
print(cf_tv7377.Ax(cf_tv7377.w), '=', cf_tv7377.msn[-1])
print(cf_tv7377.Ax(150), '=', cf_tv7377.msn[-1])

print(cf_tv7377.Ax_(30), '=', cf_tv7377.msn[-1])
print(cf_tv7377.nAx(30, 10), '=', cf_tv7377.msn[-1])
print(cf_tv7377.nAx_(30, 10), '=', cf_tv7377.msn[-1])
print(cf_tv7377.nAEx(30, 10), '=', cf_tv7377.msn[-1])
print(cf_tv7377.nAEx_(30, 10), '=', cf_tv7377.msn[-1])

print(cf_tv7377.t_Ax(30), '=', cf_tv7377.msn[-1])
print(cf_tv7377.t_Ax_(30, 5), '=', cf_tv7377.msn[-1])
print(cf_tv7377.t_nAx(30, 5, 10), '=', cf_tv7377.msn[-1])
print(cf_tv7377.t_nAx_(30, 5, 10), '=', cf_tv7377.msn[-1])
print(cf_tv7377.t_nAEx(30, 5, 10), '=', cf_tv7377.msn[-1])
print(cf_tv7377.t_nAEx_(30, 5, 10), '=', cf_tv7377.msn[-1])
print()
print(cf_tv7377.msn)
