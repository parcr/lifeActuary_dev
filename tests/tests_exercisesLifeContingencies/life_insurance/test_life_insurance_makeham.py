import numpy as np
import pytest
from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions


def test_life_insurance_129_1frac():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.life_insurance(x=129, interest_rate=5, age_first_instalment=129, terms=np.inf, fraction=1, w=129)
    q_w = 1 - mml.S(x=129, t=1)
    assert 1 / (1 + .05) == pytest.approx(a, rel=1e-12)


def test_life_insurance_129_12frac():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 129 + 10 / 12
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=12, w=129)
    assert 0.9942695630875482 == pytest.approx(a, rel=1e-12)


def test_life_insurance_129_12frac_b():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 129 + 11 / 12
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=12, w=129)
    assert 1.05 ** (-1 / 12) == pytest.approx(a, rel=1e-12)


def test_life_insurance_50_12frac_a():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 50
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=12, w=129)
    assert 0.19357445778744428 == pytest.approx(a, rel=1e-12)


def test_life_insurance_50_12frac_b():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 50 + 1 / 12
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=12, w=129)
    assert 0.19428541530458865 == pytest.approx(a, rel=1e-12)


def test_life_insurance_20_12frac_a():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 20
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=12, w=129)
    assert 0.05032843406705426 == pytest.approx(a, rel=1e-12)


def test_life_insurance_20_12frac_b():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 20 + 1 / 12
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=12, w=129)
    assert 0.05051384739868218 == pytest.approx(a, rel=1e-12)


def test_life_insurance_20_12frac_c():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 20 + 2 / 12
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=12, w=129)
    assert 0.05069999821147594 == pytest.approx(a, rel=1e-12)


def test_life_insurance_20_12frac_d():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 20 + 3 / 12
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=12, w=129)
    assert 0.05088688932089658 == pytest.approx(a, rel=1e-12)


def test_term2_life_insurance_20_1frac():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 20
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=1, w=129)
    assert 0.04921934283681906 == pytest.approx(a, rel=1e-12)


def test_term_life_insurance_20_12frac():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 20
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=12, w=129)
    assert 0.05032843406705426 == pytest.approx(a, rel=1e-12)


def test_term_life_insurance_40_1frac():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 40
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=1, w=129)
    assert 0.12105921086937971 == pytest.approx(a, rel=1e-12)


def test_term_life_insurance_40_12frac():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 40
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=12, w=129)
    assert 0.12378671275261083 == pytest.approx(a, rel=1e-12)


def test_term_life_insurance_60_1frac():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 60
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=1, w=129)
    assert 0.29028217616060503 == pytest.approx(a, rel=1e-12)


def test_term_life_insurance_60_12frac():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 60
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=12, w=129)
    assert 0.29683037981657273 == pytest.approx(a, rel=1e-12)


def test_term_life_insurance_80_1frac():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 80
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=1, w=129)
    assert 0.592933066360474 == pytest.approx(a, rel=1e-12)


def test_term_life_insurance_80_12frac():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 80
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=12, w=129)
    assert 0.6064081527838994 == pytest.approx(a, rel=1e-12)


def test_term_life_insurance_100_1frac():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 100
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=1, w=129)
    assert 0.8706841462132785 == pytest.approx(a, rel=1e-12)


def test_term_life_insurance_100_12frac():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    x0 = 100
    a = mml.life_insurance(x=x0, interest_rate=5, age_first_instalment=x0, terms=np.inf, fraction=12, w=129)
    assert 0.8915840217595198 == pytest.approx(a, rel=1e-12)
