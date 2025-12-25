from src.data.loader import load_price_data
from src.research.cointegration import engle_granger_test
from src.research.spread import compute_spread
from src.strategy.signals import compute_zscore
from src.strategy.portfolio import generate_positions

# Load prices
prices = load_price_data(["INFY.NS", "TCS.NS"])
y = prices["INFY.NS"]
x = prices["TCS.NS"]

# Cointegration
result = engle_granger_test(y, x)
beta = result["hedge_ratio"]

# Spread
spread = compute_spread(y, x, beta)

# Z-score
zscore = compute_zscore(spread)

# Positions
positions = generate_positions(zscore)

print(positions.value_counts())
