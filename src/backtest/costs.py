import pandas as pd

def apply_transaction_costs(positions: pd.Series, cost_per_trade: float = 0.0005):
    """
    Apply transaction costs based on position changes.
    """
    trades = positions.diff().abs()
    costs = trades * cost_per_trade
    return costs.fillna(0)
