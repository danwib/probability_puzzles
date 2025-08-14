def ppv(sensitivity: float, specificity: float, prevalence: float) -> float:
    """
    Positive Predictive Value:
    P(disease | positive) = sens*prev / (sens*prev + (1-spec)*(1-prev))
    """
    if not (0 <= sensitivity <= 1 and 0 <= specificity <= 1 and 0 <= prevalence <= 1):
        raise ValueError("inputs must be in [0,1]")
    num = sensitivity * prevalence
    den = num + (1 - specificity) * (1 - prevalence)
    return 0.0 if den == 0 else num / den

def npv(sensitivity: float, specificity: float, prevalence: float) -> float:
    """
    Negative Predictive Value:
    P(no disease | negative) = spec*(1-prev) / (spec*(1-prev) + (1-sens)*prev)
    """
    if not (0 <= sensitivity <= 1 and 0 <= specificity <= 1 and 0 <= prevalence <= 1):
        raise ValueError("inputs must be in [0,1]")
    num = specificity * (1 - prevalence)
    den = num + (1 - sensitivity) * prevalence
    return 0.0 if den == 0 else num / den
