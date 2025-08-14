from src.coupon_collector import expected_trials_to_collect, expected_trials_approx, harmonic_number

def test_exact_vs_known_small():
    # n=1 -> 1 draw, n=2 -> 3 draws, n=3 -> 5.5 draws
    assert expected_trials_to_collect(1) == 1.0
    assert expected_trials_to_collect(2) == 3.0
    assert abs(expected_trials_to_collect(3) - 5.5) < 1e-9

def test_approx_reasonable():
    n = 100
    exact = expected_trials_to_collect(n)
    approx = expected_trials_approx(n)
    assert abs(approx - exact) / exact < 0.02  # within ~2%
