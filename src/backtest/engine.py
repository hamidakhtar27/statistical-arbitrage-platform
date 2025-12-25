import pandas as pd

def backtest_spread_strategy(
    spread: pd.Series,
    positions: pd.Series,
    costs: pd.Series
):
    """
    Backtest mean-reversion spread strategy.
    """
    # Lag positions to avoid look-ahead bias
    positions_lagged = positions.shift(1).fillna(0)

    # Daily PnL from spread changes
    spread_returns = spread.diff().fillna(0)
    pnl = positions_lagged * spread_returns

    # Net PnL after costs
    net_pnl = pnl - costs

    equity_curve = net_pnl.cumsum()

    return pd.DataFrame({
        "positions": positions_lagged,
        "spread_returns": spread_returns,
        "pnl": pnl,
        "costs": costs,
        "net_pnl": net_pnl,
        "equity": equity_curve
    })
