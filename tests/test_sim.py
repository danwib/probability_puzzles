# tests/test_sim.py
from src.birthday import prob_shared_birthday
from src.coupon_collector import expected_trials_to_collect
from src.sim import simulate_birthday, simulate_coupon_collector


def test_birthday_sim_close():
    est = simulate_birthday(23, trials=3000, seed=1)
    theo = prob_shared_birthday(23)
    assert abs(est - theo) < 0.05  # within ~5%


def test_coupon_sim_close():
    est = simulate_coupon_collector(20, trials=400, seed=2)
    theo = expected_trials_to_collect(20)
    assert abs(est - theo) / theo < 0.08  # within ~8%
