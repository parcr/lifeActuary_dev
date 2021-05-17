import numpy as np
from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
from annuities_certain import annuities_certain

x = 65
defer = 10
interest_rate = 5
mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
wlad65_12 = mml.annuity(x=x, interest_rate=interest_rate, age_first_instalment=65, terms=np.inf, fraction=12, w=130)
nEx = mml.nEx(x=x, interest_rate=interest_rate, defer=defer)

ac = annuities_certain.Annuities_Certain(interest_rate=interest_rate, frequency=12)
ac10 = ac.annuity_due(terms=10)
