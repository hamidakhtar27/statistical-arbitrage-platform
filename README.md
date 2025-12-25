# Statistical Arbitrage Research Platform

An industry-grade quantitative research platform for **statistical arbitrage and pairs trading**, designed to mirror the workflow used by professional quant researchers and hedge funds.

This project implements **cointegration-based mean-reversion strategies** with full signal generation, portfolio construction, transaction cost modeling, backtesting, and an interactive Dash dashboard for research and evaluation.

---

## 🚀 Key Features

- Engle–Granger cointegration testing
- Mean-reverting spread construction
- Z-score based long/short signal generation
- Market-neutral portfolio construction
- Transaction cost modeling
- Full backtesting engine
- Performance analytics (Sharpe ratio, drawdown, returns)
- Interactive Dash dashboard for strategy research

---

## 🧠 Research Methodology

1. Select economically related asset pairs  
2. Test for cointegration using Engle–Granger methodology  
3. Estimate hedge ratio and construct mean-reverting spread  
4. Normalize spread into Z-score  
5. Generate long/short trading signals based on statistical thresholds  
6. Apply transaction costs and backtest the strategy  
7. Evaluate performance using institutional risk metrics  

---

## 🛠 Tech Stack

- Python 3
- NumPy, Pandas
- Statsmodels
- Plotly & Dash
- Modular research and backtesting architecture

---

## 📈 Use Cases

- Quantitative research & strategy prototyping  
- Pairs trading analysis  
- Mean-reversion strategy validation  
- Interview-ready quant finance portfolio project  

---

## ▶️ How to Run

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run dashboard
python app.py
