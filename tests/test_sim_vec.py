# tests/test_sim_vec.py
import math

from src.birthday import prob_shared_birthday
from src.coupon_collector import expected_trials_to_collect
from src.order_stats import expected_kth_uniform, expected_max_uniform

# Vectorised MC functions (added in src/sim.py)
from src.sim import (
    simulate_birthday_vec,
    simulate_coupon_collector_vec,
    simulate_empty_bins_vec,
    simulate_order_stat_k_uniform_vec,
    simulate_order_stat_max_uniform_vec,
)


def test_birthday_vec_matches_analytic_small_tol():
    n, days, trials, seed = 23, 365, 5000, 0
    analytic = prob_shared_birthday(n, days=days)
    mc = simulate_birthday_vec(n, trials=trials, days=days, seed=seed)
    assert 0 <= mc <= 1
    assert abs(analytic - mc) < 0.03  # 3% absolute tolerance keeps CI stable


def test_coupon_vec_matches_analytic_rel_tol():
    n, trials, seed = 30, 3000, 0
    analytic = expected_trials_to_collect(n)
    mc = simulate_coupon_collector_vec(n, trials=trials, seed=seed)
    rel_err = abs(analytic - mc) / analytic
    assert rel_err < 0.12  # generous for small trials, fast CI


def test_order_stats_max_vec():
    n, trials, seed = 10, 5000, 0
    analytic = expected_max_uniform(n)
    mc = simulate_order_stat_max_uniform_vec(n, trials=trials, seed=seed)
    assert abs(analytic - mc) < 0.02


def test_order_stats_k_vec():
    n, k, trials, seed = 10, 3, 8000, 0
    analytic = expected_kth_uniform(n, k)
    mc = simulate_order_stat_k_uniform_vec(n, k, trials=trials, seed=seed)
    assert abs(analytic - mc) < 0.02


def test_empty_bins_vec_reasonable():
    m, n, trials, seed = 20, 10, 5000, 0
    mc = simulate_empty_bins_vec(m, n, trials=trials, seed=seed)
    # Analytic expectation ~ n * exp(-m/n)
    approx = n * math.exp(-m / n)
    assert abs(mc - approx) < 0.3  # coarse tolerance is fine for small trials
