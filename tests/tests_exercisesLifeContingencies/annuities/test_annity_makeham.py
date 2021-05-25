import numpy as np
import pytest
from exercisesLifeContingencies.survivalModels.someMortalityLaws import makeham_mortality_functions


def test_wlad_20_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=20, interest_rate=5, age_first_instalment=20, terms=np.inf, fraction=1, w=130)
    assert 19.966393800426772 == pytest.approx(a, rel=1e-12)


def test_wlad_20_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=20, interest_rate=5, age_first_instalment=20, terms=np.inf, fraction=4, w=130)
    assert 19.58756285920462 == pytest.approx(a, rel=1e-12)


def test_wlai_20_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=20, interest_rate=5, age_first_instalment=20 + 1, terms=np.inf, fraction=1, w=130)
    assert 18.966393800426772 == pytest.approx(a, rel=1e-12)


def test_wlai_20_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=20, interest_rate=5, age_first_instalment=20 + 1 / 4, terms=np.inf, fraction=4, w=130)
    assert 19.337562859204613 == pytest.approx(a, rel=1e-12)


def test_wlad_40_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=40, interest_rate=5, age_first_instalment=40, terms=np.inf, fraction=1, w=130)
    assert 18.457756571743005 == pytest.approx(a, rel=1e-12)


def test_wlad_40_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=40, interest_rate=5, age_first_instalment=40, terms=np.inf, fraction=4, w=130)
    assert 18.078905180633175 == pytest.approx(a, rel=1e-12)


def test_wlai_40_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=40, interest_rate=5, age_first_instalment=40 + 1, terms=np.inf, fraction=1, w=130)
    assert 17.457756571743005 == pytest.approx(a, rel=1e-12)


def test_wlai_40_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=40, interest_rate=5, age_first_instalment=40 + 1 / 4, terms=np.inf, fraction=4, w=130)
    assert 17.828905180633175 == pytest.approx(a, rel=1e-12)


def test_wlad_60_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=60, interest_rate=5, age_first_instalment=60, terms=np.inf, fraction=1, w=130)
    assert 14.904074300627276 == pytest.approx(a, rel=1e-12)


def test_wlad_60_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=60, interest_rate=5, age_first_instalment=60, terms=np.inf, fraction=4, w=130)
    assert 14.525011062804799 == pytest.approx(a, rel=1e-12)


def test_wlai_60_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=60, interest_rate=5, age_first_instalment=60 + 1, terms=np.inf, fraction=1, w=130)
    assert 13.904074300627276 == pytest.approx(a, rel=1e-12)


def test_wlai_60_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=60, interest_rate=5, age_first_instalment=60 + 1 / 4, terms=np.inf, fraction=4, w=130)
    assert 14.275011062804799 == pytest.approx(a, rel=1e-12)


def test_wlad_80_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=80, interest_rate=5, age_first_instalment=80, terms=np.inf, fraction=1, w=130)
    assert 8.548405606430032 == pytest.approx(a, rel=1e-12)


def test_wlad_80_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=80, interest_rate=5, age_first_instalment=80, terms=np.inf, fraction=4, w=130)
    assert 8.167147603528539 == pytest.approx(a, rel=1e-12)


def test_wlai_80_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=80, interest_rate=5, age_first_instalment=80 + 1, terms=np.inf, fraction=1, w=130)
    assert 7.548405606430032 == pytest.approx(a, rel=1e-12)


def test_wlai_80_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=80, interest_rate=5, age_first_instalment=80 + 1 / 4, terms=np.inf, fraction=4, w=130)
    assert 7.917147603528528 == pytest.approx(a, rel=1e-12)


'''
temp annuities
'''


def test_tad_20_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=20, interest_rate=5, age_first_instalment=20, terms=10, fraction=1, w=130)
    assert 8.099143695034797 == pytest.approx(a, rel=1e-12)


def test_tad_20_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=20, interest_rate=5, age_first_instalment=20, terms=10, fraction=4, w=130)
    assert 7.952250811733334 == pytest.approx(a, rel=1e-12)


def test_tai_20_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=20, interest_rate=5, age_first_instalment=20 + 1, terms=10, fraction=1, w=130)
    assert 7.711382730455226 == pytest.approx(a, rel=1e-12)


def test_tai_20_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=20, interest_rate=5, age_first_instalment=20 + 1 / 4, terms=10, fraction=4, w=130)
    assert 7.855310570588442 == pytest.approx(a, rel=1e-12)


''''''


def test_tad_40_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=40, interest_rate=5, age_first_instalment=40, terms=10, fraction=1, w=130)
    assert 8.086328661846537 == pytest.approx(a, rel=1e-12)


def test_tad_40_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=40, interest_rate=5, age_first_instalment=40, terms=10, fraction=4, w=130)
    assert 7.938305938401428 == pytest.approx(a, rel=1e-12)


def test_tai_40_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=40, interest_rate=5, age_first_instalment=40 + 1, terms=10, fraction=1, w=130)
    assert 7.695533433095565 == pytest.approx(a, rel=1e-12)


def test_tai_40_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=40, interest_rate=5, age_first_instalment=40 + 1 / 4, terms=10, fraction=4, w=130)
    assert 7.840607131213686 == pytest.approx(a, rel=1e-12)


''''''


def test_tad_60_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=60, interest_rate=5, age_first_instalment=60, terms=10, fraction=1, w=130)
    assert 7.955548143878779 == pytest.approx(a, rel=1e-12)


def test_tad_60_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=60, interest_rate=5, age_first_instalment=60, terms=10, fraction=4, w=130)
    assert 7.796128394417279 == pytest.approx(a, rel=1e-12)


def test_tai_60_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=60, interest_rate=5, age_first_instalment=60 + 1, terms=10, fraction=1, w=130)
    assert 7.534191594775955 == pytest.approx(a, rel=1e-12)


def test_tai_60_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=60, interest_rate=5, age_first_instalment=60 + 1 / 4, terms=10, fraction=4, w=130)
    assert 7.690789257141573 == pytest.approx(a, rel=1e-12)


''''''


def test_tad_80_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=80, interest_rate=5, age_first_instalment=80, terms=10, fraction=1, w=130)
    assert 6.788520800665058 == pytest.approx(a, rel=1e-12)


def test_tad_80_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=80, interest_rate=5, age_first_instalment=80, terms=10, fraction=4, w=130)
    assert 6.538535827831598 == pytest.approx(a, rel=1e-12)


def test_tai_80_1term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=80, interest_rate=5, age_first_instalment=80 + 1, terms=10, fraction=1, w=130)
    assert 6.1280362723202835 == pytest.approx(a, rel=1e-12)


def test_tai_80_4term():
    mml = makeham_mortality_functions.Makeham(a=0.00022, b=2.7E-6, c=1.124)
    a = mml.annuity(x=80, interest_rate=5, age_first_instalment=80 + 1 / 4, terms=10, fraction=4, w=130)
    assert 6.373414695745405 == pytest.approx(a, rel=1e-12)
