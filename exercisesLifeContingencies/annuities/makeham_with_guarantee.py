import numpy as np
from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions
from annuities_certain import annuities_certain

x = 65
defer = 10
interest_rate = 5
mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
wlad65_12 = mml.annuity(x=x, interest_rate=interest_rate, age_first_instalment=65, terms=np.inf, fraction=12, w=130)
wlad75_12 = mml.annuity(x=x + defer, interest_rate=interest_rate, age_first_instalment=x + defer,
                        terms=np.inf, fraction=12, w=130)
nEx = mml.nEx(x=x, interest_rate=interest_rate, defer=defer)

ac = annuities_certain.Annuities_Certain(interest_rate=interest_rate, m=12)
ac10 = ac.aan(terms=10)

wlad65_12_10 = mml.annuity(x=x, interest_rate=interest_rate, age_first_instalment=65, terms=10, fraction=12, w=130)
test_wlad65_12 = wlad65_12_10 + nEx * wlad75_12
test_wlad75_12 = mml.annuity(x=x, interest_rate=interest_rate, age_first_instalment=x + defer,
                             terms=np.inf, fraction=12, w=130)
test_wlad65_12_defer_10 = nEx * wlad75_12

B = 12000 * wlad65_12 / (ac10 + nEx * wlad75_12)
