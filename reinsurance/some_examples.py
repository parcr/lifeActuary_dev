import reinsurance_types as rt
import numpy as np
import matplotlib.pyplot as plt

qs = rt.QuotaShare(cedant_share=0.1, total_capacity=1E7, capital_at_risk=2.5E6)
sp = rt.Surplus(cedant_line=1E6, total_capacity=1E7, capital_at_risk=2.5E6)
xsl=rt.ExcessOfLoss(cedant_retention=1E6, total_capacity=1E7)
