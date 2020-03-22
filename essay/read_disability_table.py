__author__ = "PedroCR"

from disability_tables import disability_tables as dt
from turnover_tables import turnover_tables as tt
import mortality_table as mt

ekv80 = dt.EVK_80
ekv80_70 = dt.EVK_80_ext_70
pcr1 = tt.pcr_turnover
pcr2 = tt.pcr_turnover_65

dt_ekv80 = mt.MortalityTable(mt=ekv80)
dt_ekv80.force_qw_0()
tt_pcr = mt.MortalityTable(mt=pcr1)
tt_pcr.force_qw_0()
