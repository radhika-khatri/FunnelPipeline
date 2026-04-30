import math
from scipy.stats import norm

def sample_size(p1, p2, power=0.8, alpha=0.05):
    z_alpha = norm.ppf(1 - alpha/2)
    z_beta = norm.ppf(power)

    p = (p1 + p2) / 2

    num = (z_alpha * (2*p*(1-p))**0.5 + z_beta * (p1*(1-p1)+p2*(1-p2))**0.5)**2
    den = (p2 - p1)**2

    return int(num/den)


def attach_sample_size(experiments, funnel):
    base = funnel["signup_form"]["conversion_rate"]

    for e in experiments:
        new = base + e["minimum_detectable_effect"]
        e["baseline_conversion_rate"] = base
        e["sample_size_per_arm"] = sample_size(base, new)

    return experiments