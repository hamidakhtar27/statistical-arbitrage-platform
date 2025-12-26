import numpy as np
import pandas as pd


def backtest_portfolio(
    prices: pd.DataFrame,
    spread: pd.Series,
    signals: pd.Series,
    transaction_cost: float = 0.0005
) -> pd.DataFrame:
    """
    Backtest a market-neutral spread trading strategy.

    Parameters
    ----------
    prices : pd.DataFrame
        Price series of the two assets.
    spread : pd.Series
        Cointegrated spread.
    signals : pd.Series
        Trading signals (+1 long, -1 short, 0 flat).
    transaction_cost : float
        Proportional transaction cost per trade.

    Returns
    -------
    pd.DataFrame
        Portfolio performance with equity curve and drawdown.
    """

    # Align everything
    signals = signals.reindex(spread.index).fillna(0)

    # Spread returns
    spread_returns = spread.diff().fillna(0)

    # Strategy PnL
    pnl = signals.shift(1) * spread_returns

    # Transaction costs
    trades = signals.diff().abs()
    costs = trades * transaction_cost

    net_pnl = pnl - costs

    # Equity curve
    equity = net_pnl.cumsum()

    # Drawdown
    rolling_max = equity.cummax()
    drawdown = equity - rolling_max

    return pd.DataFrame({
        "equity_curve": equity,
        "drawdown": drawdown,
        "pnl": net_pnl
    })
