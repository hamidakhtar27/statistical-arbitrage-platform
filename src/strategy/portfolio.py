import pandas as pd

def generate_positions(zscore: pd.Series, entry: float = 2.0, exit: float = 0.5):
    """
    Generate long/short signals based on Z-score.
    """
    positions = pd.Series(0, index=zscore.index)

    positions[zscore > entry] = -1   # Short spread
    positions[zscore < -entry] = 1   # Long spread
    positions[abs(zscore) < exit] = 0

    return positions
