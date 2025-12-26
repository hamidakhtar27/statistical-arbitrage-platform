import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

def load_price_data(
    tickers,
    pair_name,
    use_local=True,
    start=None,
    end=None
):
    """
    Production-safe price loader.
    Defaults to local cached CSVs.
    """

    if use_local:
        file_path = DATA_DIR / f"{pair_name}.csv"

        if not file_path.exists():
            raise FileNotFoundError(f"Missing local data file: {file_path}")

        df = pd.read_csv(file_path, index_col=0, parse_dates=True)
        df = df[tickers].dropna()
        return df

    # Research-only fallback
    import yfinance as yf
    df = yf.download(tickers, start=start, end=end)["Adj Close"]
    return df.dropna()
