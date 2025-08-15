def expected_max_uniform(n: int) -> float:
    """
    E[max of n i.i.d. Uniform(0,1)] = n/(n+1)
    """
    if n <= 0:
        raise ValueError("n must be positive")
    return n / (n + 1)


def expected_kth_uniform(n: int, k: int) -> float:
    """
    E[k-th order stat of n i.i.d. Uniform(0,1)] = k/(n+1), 1 <= k <= n
    """
    if not (1 <= k <= n):
        raise ValueError("require 1 <= k <= n")
    return k / (n + 1)
