import math


def harmonic_number(n: int) -> float:
    return sum(1.0 / k for k in range(1, n + 1))


def expected_trials_to_collect(n: int) -> float:
    """
    Expected draws to collect all n coupon types with uniform sampling: n * H_n.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    return n * harmonic_number(n)


def expected_trials_approx(n: int) -> float:
    """
    Asymptotic: n * (ln n + gamma) + 0.5 with Euler–Mascheroni gamma.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    gamma = 0.5772156649015329
    return n * (math.log(n) + gamma) + 0.5
