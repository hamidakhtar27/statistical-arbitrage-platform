import numpy as np
import pandas as pd

def estimate_ou_params(spread: pd.Series):
    """
    Estimate OU parameters using AR(1) approximation.
    dX = theta(mu - X)dt + sigma dW
    """
    spread_lag = spread.shift(1).dropna()
    spread_curr = spread.loc[spread_lag.index]

    # Linear regression X_t = a + b X_{t-1}
    b, a = np.polyfit(spread_lag, spread_curr, 1)

    theta = -np.log(b)
    mu = a / (1 - b)
    sigma = spread_curr.std()

    return {
        "theta": theta,
        "mu": mu,
        "sigma": sigma
    }
