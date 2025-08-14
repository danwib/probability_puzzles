import math

def prob_shared_birthday(n: int, days: int = 365) -> float:
    """
    Probability that at least two people share a birthday in a group of n,
    assuming 'days' equally likely birthdays and independence.
    """
    if n <= 1:
        return 0.0
    if n > days:
        return 1.0
    log_p_all_distinct = 0.0
    for k in range(n):
        log_p_all_distinct += math.log((days - k) / days)
    p_all_distinct = math.exp(log_p_all_distinct)
    return 1.0 - p_all_distinct

