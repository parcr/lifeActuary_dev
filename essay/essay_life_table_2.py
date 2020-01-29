# author: PedroCR #
from toDelete.mortality_tables_old import TV7377, GKM95_lx_15
import mortality_table
import commutation_table

lt_tv7377 = mortality_table.MortalityTable(mt=TV7377)
lt_gkm95 = mortality_table.MortalityTable(data_type='l', mt=GKM95_lx_15)
cf_tv7377 = commutation_table.CommutationFunctions(i=2, g=1.5, mt=TV7377)
print(cf_tv7377.df_commutation_table())
print(cf_tv7377.aax(25), cf_tv7377.msn[-1])