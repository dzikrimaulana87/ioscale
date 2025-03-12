import numpy as np
from scipy import stats

def confidence_interval(data, confidence=0.95):
    
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    alpha = 1 - confidence
    
    if n >= 30:
        z_critical = stats.norm.ppf(1 - alpha/2)
        margin_of_error = z_critical * (std / np.sqrt(n))
    else:
        t_critical = stats.t.ppf(1 - alpha/2, df=n-1)
        margin_of_error = t_critical * (std / np.sqrt(n))

    lower_bound = mean - margin_of_error
    upper_bound = mean + margin_of_error

    return f"Rp {lower_bound:,.0f}".replace(",", "."), f"Rp {upper_bound:,.0f}".replace(",", ".")