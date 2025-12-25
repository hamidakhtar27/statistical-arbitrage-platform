import numpy as np
import pandas as pd

def compute_performance_metrics(equity: pd.Series, pnl: pd.Series):
    """
    Compute core performance metrics.
    """
    returns = pnl

    sharpe = np.sqrt(252) * returns.mean() / returns.std()
    max_dd = (equity - equity.cummax()).min()
    total_return = equity.iloc[-1]

    return {
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_dd,
        "Total Return": total_return
    }
