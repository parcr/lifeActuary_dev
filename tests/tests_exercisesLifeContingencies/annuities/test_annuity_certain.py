import pytest
from annuities_certain import annuities_certain as ac


def test_annuity_due():
    renda = ac.Annuities_Certain(interest_rate=5, frequency=1)
    r1 = renda.annuity_due(10)
    assert 8.107821675644 == pytest.approx(r1, rel=1e-12)


def test_annuity_immediate():
    renda = ac.Annuities_Certain(interest_rate=5, frequency=1)
    r1 = renda.annuity_immediate(10)
    assert 7.721734929185 == pytest.approx(r1, rel=1e-12)


def test_annuity_due_m():
    renda = ac.Annuities_Certain(interest_rate=5, frequency=12)
    r1 = renda.annuity_due(10)
    assert 7.929306443990 == pytest.approx(r1, rel=1e-12)


def test_annuity_immediate_m():
    renda = ac.Annuities_Certain(interest_rate=5, frequency=12)
    r1 = renda.annuity_immediate(10)
    assert 7.897132548452 == pytest.approx(r1, rel=1e-12)


def test_annuity_due_m2():
    renda = ac.Annuities_Certain(interest_rate=5, frequency=4)
    r1 = renda.annuity_due(10)
    assert 7.961567548713 == pytest.approx(r1, rel=1e-12)


def test_annuity_immediate_m2():
    renda = ac.Annuities_Certain(interest_rate=5, frequency=4)
    r1 = renda.annuity_immediate(10)
    assert 7.865045862098 == pytest.approx(r1, rel=1e-12)
