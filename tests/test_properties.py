from src.coupon_collector import expected_trials_to_collect
from src.order_stats import expected_max_uniform

def test_coupon_monotone_in_n():
    assert expected_trials_to_collect(10) < expected_trials_to_collect(20)

def test_order_stats_bounds():
    # E[max U(0,1) of n] is in (0,1) and increases with n
    e1, e2 = expected_max_uniform(1), expected_max_uniform(5)
    assert 0 < e1 < 1 and 0 < e2 < 1 and e1 < e2
