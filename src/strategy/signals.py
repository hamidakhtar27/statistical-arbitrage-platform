import pandas as pd

def compute_zscore(spread: pd.Series, window: int = 60):
    """
    Compute rolling Z-score of the spread.
    """
    rolling_mean = spread.rolling(window).mean()
    rolling_std = spread.rolling(window).std()
    zscore = (spread - rolling_mean) / rolling_std
    return zscore
