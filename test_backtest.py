from src.data.loader import load_price_data
from src.research.cointegration import engle_granger_test
from src.research.spread import compute_spread
from src.strategy.signals import compute_zscore
from src.strategy.portfolio import generate_positions
from src.backtest.costs import apply_transaction_costs
from src.backtest.engine import backtest_spread_strategy
from src.analytics.performance import compute_performance_metrics

# Load data
prices = load_price_data(["INFY.NS", "TCS.NS"])
y = prices["INFY.NS"]
x = prices["TCS.NS"]

# Research
coint = engle_granger_test(y, x)
beta = coint["hedge_ratio"]
spread = compute_spread(y, x, beta)

# Strategy
zscore = compute_zscore(spread)
positions = generate_positions(zscore)

# Costs
costs = apply_transaction_costs(positions)

# Backtest
results = backtest_spread_strategy(spread, positions, costs)

# Metrics
metrics = compute_performance_metrics(
    results["equity"],
    results["net_pnl"]
)

print(metrics)
