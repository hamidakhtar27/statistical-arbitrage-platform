from src.data.loader import load_price_data
from src.research.cointegration import engle_granger_test

# Load data
prices = load_price_data(["INFY.NS", "TCS.NS"])

y = prices["INFY.NS"]
x = prices["TCS.NS"]

# Run test
result = engle_granger_test(y, x)

print("Hedge Ratio:", result["hedge_ratio"])
print("ADF Statistic:", result["adf_stat"])
print("p-value:", result["p_value"])
