def expected_empty_bins(m: int, n: int) -> float:
    """
    Throw m balls uniformly at random into n bins.
    E[# empty bins] = n * (1 - 1/n)^m
    """
    if n <= 0 or m < 0:
        raise ValueError("n>0 and m>=0 required")
    return n * (1 - 1 / n) ** m
