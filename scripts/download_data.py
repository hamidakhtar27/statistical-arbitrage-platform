import yfinance as yf
import pandas as pd
from pathlib import Path

PAIRS = {
    "INFY_TCS": ["INFY.NS", "TCS.NS"],
    "HDFCBANK_ICICI": ["HDFCBANK.NS", "ICICIBANK.NS"],
    "RELIANCE_ONGC": ["RELIANCE.NS", "ONGC.NS"],
}

OUT_DIR = Path("data")
OUT_DIR.mkdir(parents=True, exist_ok=True)

for name, tickers in PAIRS.items():
    print(f"Downloading {name}...")
    
    df = yf.download(
        tickers,
        start="2018-01-01",
        end="2024-12-31",
        auto_adjust=True,
        progress=False
    )

    prices = df["Close"]
    prices.to_csv(OUT_DIR / f"{name}.csv")

print("✅ All data downloaded and saved locally.")
