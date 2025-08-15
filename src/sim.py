import numpy as np


def simulate_birthday(n: int, trials: int = 10000, days: int = 365, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(trials):
        b = rng.integers(0, days, size=n)
        hits += int(len(set(b)) < n)
    return hits / trials


def simulate_coupon_collector(n: int, trials: int = 2000, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    tot = 0
    for _ in range(trials):
        seen = np.zeros(n, dtype=bool)
        steps = 0
        while not seen.all():
            seen[rng.integers(0, n)] = True
            steps += 1
        tot += steps
    return tot / trials

def simulate_birthday_vec(n: int, trials: int = 5000, days: int = 365, seed: int = 0) -> float:
    """
    Vectorised: draw all birthdays for all trials at once, sort each row,
    detect adjacent duplicates. Returns fraction of trials with a collision.
    """
    rng = np.random.default_rng(seed)
    samples = rng.integers(0, days, size=(trials, n))
    samples.sort(axis=1)  # C-level sort (fast)
    has_dup = (samples[:, 1:] == samples[:, :-1]).any(axis=1)
    return has_dup.mean()

def simulate_coupon_collector_vec(n: int, trials: int = 3000, seed: int = 0) -> float:
    """
    Vectorised via stage decomposition: T_n = sum_{k=1..n} Geometric(p_k), p_k = k/n.
    Draw a (trials, n) matrix of geometric samples and sum rows; return mean.
    numpy.geometric returns number of trials (1-based) until success, which is exactly what we need.
    """
    rng = np.random.default_rng(seed)
    p = np.arange(1, n + 1, dtype=float) / n  # shape (n,)
    geos = rng.geometric(p, size=(trials, n))  # shape (trials, n)
    return geos.sum(axis=1).mean()

# (Optional) Vectorised MCs for other puzzles — handy if you want them in RESULTS.md too

def simulate_order_stat_max_uniform_vec(n: int, trials: int = 10000, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    x = rng.random(size=(trials, n))
    return x.max(axis=1).mean()

def simulate_order_stat_k_uniform_vec(n: int, k: int, trials: int = 10000, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    x = rng.random(size=(trials, n))
    x.sort(axis=1)
    return x[:, k - 1].mean()  # k-th smallest, 1-indexed

def simulate_empty_bins_vec(m: int, n: int, trials: int = 5000, seed: int = 0) -> float:
    """
    Throw m balls into n bins uniformly at random. For each trial, count empty bins.
    Vectorised using advanced indexing to scatter into a (trials, n) boolean occupancy matrix.
    Fine for the sizes you use (<= 100 x 50); increase trials with caution for very large n.
    """
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(trials, m))        # (trials, m)
    occ = np.zeros((trials, n), dtype=bool)           # (trials, n)
    rows = np.arange(trials)[:, None]                 # (trials, 1)
    occ[rows, idx] = True                             # mark visited bins
    empty = n - occ.sum(axis=1)                       # per-trial empty bin count
    return empty.mean()