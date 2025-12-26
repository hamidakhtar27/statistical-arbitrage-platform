import numpy as np
import pandas as pd


def generate_signals(
    zscore: pd.Series,
    entry_z: float,
    exit_z: float
) -> pd.Series:
    """
    Generate trading signals based on Z-score thresholds.

    Parameters
    ----------
    zscore : pd.Series
        Z-score time series of the cointegrated spread.
    entry_z : float
        Absolute Z-score threshold to enter trades.
    exit_z : float
        Absolute Z-score threshold to exit trades.

    Returns
    -------
    pd.Series
        Trading signal series:
        +1 = Long spread
        -1 = Short spread
         0 = Flat / Exit
    """

    if zscore is None or zscore.empty:
        return pd.Series(dtype=float)

    signals = np.zeros(len(zscore))

    # Long entry: spread too low
    signals[zscore < -entry_z] = 1

    # Short entry: spread too high
    signals[zscore > entry_z] = -1

    # Exit condition: mean reversion zone
    signals[np.abs(zscore) < exit_z] = 0

    return pd.Series(signals, index=zscore.index, name="signal")
