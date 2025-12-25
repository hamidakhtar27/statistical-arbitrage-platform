import yfinance as yf
import pandas as pd
import numpy as np

def load_price_data(tickers, start="2018-01-01", end=None):
    """
    Download adjusted close prices and return log prices.
    Works correctly for single and multiple tickers.
    """
    raw_data = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False
    )

    # Extract Adjusted Close safely
    if isinstance(raw_data.columns, pd.MultiIndex):
        adj_close = raw_data["Adj Close"]
    else:
        adj_close = raw_data[["Adj Close"]]

    adj_close = adj_close.dropna()
    log_prices = np.log(adj_close)

    return log_prices
