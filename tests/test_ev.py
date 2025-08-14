from src.ev import ev_fair_die, geometric_expected_trials

def test_ev_die():
    assert abs(ev_fair_die() - 3.5) < 1e-9

def test_geo():
    assert geometric_expected_trials(0.5) == 2.0
