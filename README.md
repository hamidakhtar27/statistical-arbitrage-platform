📈 Statistical Arbitrage Research Platform

An industry-grade statistical arbitrage research platform implementing cointegration-based pairs trading with a fully interactive Dash dashboard and stable production deployment.

🔗 Live Dashboard (Render):
https://statistical-arbitrage-platform.onrender.com/

🚀 Overview

This project implements a systematic pairs trading framework using classical quantitative finance techniques:

Engle–Granger cointegration testing

Mean-reverting spread modeling

Z-score–based trading signals

Vectorized backtesting engine

Performance analytics (Sharpe, drawdown, returns)

Interactive research dashboard (Dash + Plotly)

The platform is designed to reflect real-world quant research workflows, including data caching, reproducibility, and production-safe deployment.

🧠 Strategy Methodology
1️⃣ Pair Selection

Predefined equity pairs with economic intuition:

INFY – TCS (IT services)

HDFCBANK – ICICIBANK (banking)

RELIANCE – ONGC (energy)

2️⃣ Cointegration Test

Uses Engle–Granger two-step method

Estimates hedge ratio via OLS regression

Ensures spread stationarity before trading

3️⃣ Spread Construction
Spread
𝑡
=
𝑦
𝑡
−
𝛽
𝑥
𝑡
Spread
t
	​

=y
t
	​

−βx
t
	​


Where:

𝑦
𝑡
,
𝑥
𝑡
y
t
	​

,x
t
	​

 = asset prices

𝛽
β = hedge ratio

4️⃣ Signal Generation

Rolling Z-score of the spread

Entry when 
∣
𝑍
∣
>
𝑍
entry
∣Z∣>Z
entry
	​


Exit when 
∣
𝑍
∣
<
𝑍
exit
∣Z∣<Z
exit
	​


Configurable via dashboard sliders.

5️⃣ Backtesting Engine

Fully vectorized execution

Long/short neutral exposure

Position sizing via hedge ratio

Realistic PnL computation

6️⃣ Performance Metrics

Sharpe Ratio

Maximum Drawdown

Total Return

Equity curve & drawdown visualization

🖥️ Interactive Dashboard (Dash)

Features:

Pair selector

Entry / Exit Z-score sliders

Rolling window control

Spread & Z-score visualization

Equity curve & drawdown analysis

Live metric updates

Built using:

Dash

Plotly

Python

📂 Project Structure
statistical-arbitrage-platform/
│
├── app.py                 # Dash application (entry point)
├── requirements.txt
├── README.md
│
├── data/                  # Cached production data (NO APIs in prod)
│   ├── INFY_TCS.csv
│   ├── HDFCBANK_ICICI.csv
│   └── RELIANCE_ONGC.csv
│
├── scripts/
│   └── download_data.py   # One-time Yahoo download (research only)
│
├── src/
│   ├── data/
│   │   └── loader.py
│   ├── research/
│   │   ├── cointegration.py
│   │   ├── spread.py
│   │   ├── half_life.py
│   │   └── ou_model.py
│   ├── strategy/
│   │   ├── signals.py
│   │   └── portfolio.py
│   ├── backtest/
│   │   ├── engine.py
│   │   └── costs.py
│   └── analytics/
│       └── performance.py
│
└── tests/
    ├── test_data.py
    ├── test_cointegration.py
    ├── test_strategy.py
    └── test_backtest.py

🛡️ Production Design Choices (Important)
✅ Local Cached Data (Industry Practice)

Yahoo Finance used only once

CSVs committed for reproducibility

Zero API calls in production

No rate-limit risk

This mirrors hedge fund research demos and academic submissions.

🌐 Deployment
Platform

Render (Web Service)

Why Render?

Stable Python hosting

Simple GitHub integration

Ideal for Dash applications

Start Command
python app.py

⚙️ Local Setup
git clone https://github.com/hamidakhtar27/statistical-arbitrage-platform.git
cd statistical-arbitrage-platform

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python app.py


Then open:

http://127.0.0.1:8050

📌 Limitations & Extensions

Current:

Transaction costs simplified

Static pair universe

No leverage constraints

Planned Extensions:

Kalman filter hedge ratio

Dynamic pair discovery

ML-based regime detection

Intraday extensions

🎯 Why This Project Matters

This project demonstrates:

Quantitative finance fundamentals

Statistical modeling

Clean software architecture

Deployment maturity

Research-to-production thinking

It is intentionally built to be interview-explainable, academically defensible, and industry-relevant.

👤 Author

Mohd Hamid Akhtar Khan
Final-year B.Tech (CSE)
Aspiring Quantitative Researcher / Trader

GitHub: https://github.com/hamidakhtar27