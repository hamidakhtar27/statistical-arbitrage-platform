from src.data.loader import load_price_data
from src.research.cointegration import engle_granger_test
from src.research.spread import compute_spread
from src.research.ou_model import estimate_ou_params
from src.research.half_life import calculate_half_life

# Load data
prices = load_price_data(["INFY.NS", "TCS.NS"])

y = prices["INFY.NS"]
x = prices["TCS.NS"]

# Cointegration
coint_result = engle_granger_test(y, x)
beta = coint_result["hedge_ratio"]

# Spread
spread = compute_spread(y, x, beta)

# OU params
ou_params = estimate_ou_params(spread)
half_life = calculate_half_life(ou_params["theta"])

print("OU Parameters")
print("Theta (speed):", ou_params["theta"])
print("Mu (mean):", ou_params["mu"])
print("Sigma (vol):", ou_params["sigma"])
print("Half-life (days):", half_life)
