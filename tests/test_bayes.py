from src.bayes import ppv, npv

def test_basic_values():
    sens, spec, prev = 0.9, 0.95, 0.1
    p = ppv(sens, spec, prev)
    n = npv(sens, spec, prev)
    assert 0 <= p <= 1 and 0 <= n <= 1
    # Higher prevalence should increase PPV
    assert ppv(sens, spec, 0.2) > p
