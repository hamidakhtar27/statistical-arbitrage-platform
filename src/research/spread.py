import pandas as pd

def compute_spread(y: pd.Series, x: pd.Series, hedge_ratio: float):
    """
    Construct the cointegrated spread.
    Spread = y - beta * x
    """
    y, x = y.align(x, join="inner")
    spread = y - hedge_ratio * x
    return spread
