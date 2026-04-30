
# Sample Size Model

We compute sample size for A/B testing using a two-proportion z-test.

## Parameters

- Significance level (alpha): 0.05
- Power: 0.8
- Two-sided test

## Formula

n = 2 * (Z_alpha/2 + Z_beta)^2 * p * (1 - p) / (delta^2)

Where:

- Z_alpha/2 = 1.96 (for 95% confidence)
- Z_beta = 0.84 (for 80% power)
- p = baseline conversion rate
- delta = minimum detectable effect (MDE)

## Interpretation

- Larger MDE -> smaller sample size
- Smaller baseline -> larger sample size
- Ensures statistically reliable experiment results
