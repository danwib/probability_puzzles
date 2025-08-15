import math
from src.sim import simulate_birthday, simulate_coupon_collector
from src.birthday import prob_shared_birthday
from src.coupon_collector import expected_trials_to_collect

def test_birthday_mc_matches_analytic():
    n, days, trials = 23, 365, 5000
    analytic = prob_shared_birthday(n, days=days)
    mc = simulate_birthday(n, trials=trials, days=days, seed=1)
    assert abs(analytic - mc) < 0.05  # ~5% absolute tolerance

def test_coupon_mc_matches_analytic():
    n, trials = 30, 1000
    analytic = expected_trials_to_collect(n)
    mc = simulate_coupon_collector(n, trials=trials, seed=1)
    rel_err = abs(analytic - mc) / analytic
    assert rel_err < 0.15  # 15% relative tolerance to keep CI stable
