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
        seen = np.zeros(n, dtype=bool); steps = 0
        while not seen.all():
            seen[rng.integers(0, n)] = True
            steps += 1
        tot += steps
    return tot / trials
