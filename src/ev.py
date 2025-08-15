import math


def ev_fair_die():
    return sum(range(1, 7)) / 6


def geometric_expected_trials(p: float) -> float:
    if not (0 < p <= 1):
        raise ValueError("p in (0,1]")
    return 1.0 / p
