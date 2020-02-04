__author__ = "PedroCR"

import annuities
import mortality_table as mt

from soa_tables import read_soa_table_xml as rst

soa_TV7377 = rst.SoaTable('../soa_tables/TV7377.xml')
soa_GRF95 = rst.SoaTable('../soa_tables/GRF95.xml')
mt_GRF95 = mt.MortalityTable(mt=soa_GRF95.table_qx)
mt_TV7377 = mt.MortalityTable(mt=soa_TV7377.table_qx)

a1 = annuities.axy(mtx=mt_GRF95, mty=mt_TV7377, x=45, y=45.7, i=2, g=0, m=14)
a2 = annuities.axy(mtx=mt_GRF95, mty=mt_TV7377, x=45, y=45.7, i=2, g=0, m=1)
print(a1)
print(a2)
