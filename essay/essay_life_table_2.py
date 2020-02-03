# author: PedroCR #
from soa_tables import read_soa_table_xml as rst
import mortality_table
import commutation_table

mt_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
mt_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')

lt_tv7377 = mortality_table.MortalityTable(mt=mt_TV7377.table_qx)
lt_gRF95 = mortality_table.MortalityTable(mt=mt_GRF95.table_qx)
cf_tv7377 = commutation_table.CommutationFunctions(i=1.4, g=1, mt=mt_TV7377.table_qx)
cf_grf95 = commutation_table.CommutationFunctions(i=1.4, g=1, mt=mt_GRF95.table_qx)
# print(cf_tv7377.df_commutation_table())
print(cf_grf95.aax(63))
