from src.data.loader import load_price_data

prices = load_price_data(["INFY.NS", "TCS.NS"])
print(prices.head())
