import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

def engle_granger_test(y: pd.Series, x: pd.Series):
    """
    Perform Engle–Granger cointegration test.

    Parameters
    ----------
    y : pd.Series
        Dependent variable (log price of asset A)
    x : pd.Series
        Independent variable (log price of asset B)

    Returns
    -------
    dict
        hedge_ratio : float
        adf_stat    : float
        p_value     : float
        residuals  : pd.Series
    """

    # Ensure aligned index
    y, x = y.align(x, join="inner")

    # OLS regression: y = beta * x + c
    x_const = sm.add_constant(x)
    model = sm.OLS(y, x_const).fit()

    hedge_ratio = model.params.iloc[1]
    residuals = model.resid

    # ADF test on residuals
    adf_stat, p_value, _, _, _, _ = adfuller(residuals)

    return {
        "hedge_ratio": hedge_ratio,
        "adf_stat": adf_stat,
        "p_value": p_value,
        "residuals": residuals
    }
