# 📈 Statistical Arbitrage Research Platform

An industry-grade **quantitative trading research project** implementing cointegration-based statistical arbitrage (pairs trading) with systematic signal generation, vectorized backtesting, and performance analytics.  
The project is deployed as an interactive **Dash research dashboard** with stable, production-safe data handling.

🔗 **Live Dashboard (Render)**  
https://statistical-arbitrage-platform.onrender.com/

---

## Overview

This project implements a **production-style statistical arbitrage research platform** designed to mirror real-world quantitative workflows used in hedge funds and proprietary trading desks.

Rather than focusing only on theoretical mean-reversion concepts, the platform emphasizes:

- Rigorous statistical validation of trading relationships  
- Robust spread construction and normalization  
- Systematic, rule-based signal generation  
- Full backtesting with risk and performance evaluation  
- Interactive research and parameter exploration  

The result is a **complete research-to-deployment system**, not just a standalone trading strategy.

---

## Quantitative Methods Implemented

- Engle–Granger cointegration testing for pair validation  
- OLS-based hedge ratio estimation  
- Mean-reverting spread construction  
- Rolling Z-score normalization  
- Threshold-based long/short signal generation  
- Vectorized portfolio backtesting  
- Risk-adjusted performance metrics  

---

## Strategy Workflow

### 1️⃣ Pair Selection

Predefined equity pairs with clear economic intuition:

- **INFY – TCS** (IT services sector)  
- **HDFCBANK – ICICIBANK** (Indian banking sector)  
- **RELIANCE – ONGC** (Energy sector)  

---

### 2️⃣ Cointegration Testing

- Uses the **Engle–Granger two-step methodology**  
- Hedge ratio estimated via OLS regression  
- Ensures spread stationarity before strategy execution  

---

### 3️⃣ Spread Construction

The trading spread is defined as:

Spread_t = y_t − β x_t

yaml
Copy code

Where:

- `y_t`, `x_t` = asset prices  
- `β` = hedge ratio  

---

### 4️⃣ Signal Generation

- Rolling Z-score of the spread  
- **Entry:** |Z| > Z_entry  
- **Exit:** |Z| < Z_exit  

All parameters are configurable via dashboard controls.

---

### 5️⃣ Backtesting Engine

- Fully vectorized execution  
- Market-neutral long/short exposure  
- Hedge-ratio–adjusted position sizing  
- Realistic PnL and equity curve computation  

---

### 6️⃣ Performance Metrics

- Sharpe Ratio  
- Maximum Drawdown  
- Total Return  
- Equity curve and drawdown visualization  

---

## Interactive Research Dashboard

The dashboard enables real-time research through:

- Asset pair selector  
- Entry / exit Z-score sliders  
- Rolling window adjustment  
- Spread and Z-score visualization  
- Equity curve and drawdown analysis  
- Live performance metric updates  

**Built using:**

- Dash  
- Plotly  
- Python  

---

## Project Structure

statistical-arbitrage-platform/
│
├── app.py # Dash application (entry point)
├── requirements.txt
├── README.md
│
├── data/ # Cached production data (NO APIs in production)
│ ├── INFY_TCS.csv
│ ├── HDFCBANK_ICICI.csv
│ └── RELIANCE_ONGC.csv
│
├── scripts/
│ └── download_data.py # One-time Yahoo download (research only)
│
├── src/
│ ├── data/
│ │ └── loader.py
│ ├── research/
│ │ ├── cointegration.py
│ │ ├── spread.py
│ │ ├── half_life.py
│ │ └── ou_model.py
│ ├── strategy/
│ │ ├── signals.py
│ │ └── portfolio.py
│ ├── backtest/
│ │ ├── engine.py
│ │ └── costs.py
│ └── analytics/
│ └── performance.py
│
└── tests/
├── test_data.py
├── test_cointegration.py
├── test_strategy.py
└── test_backtest.py

yaml
Copy code

---

## Production Design Choices

### Cached Local Market Data (Industry Practice)

- Yahoo Finance used only once for offline data acquisition  
- Price data stored as CSVs for reproducibility  
- Zero external API calls in production  
- No rate-limit or availability risk  

This mirrors professional quant research demos and academic evaluation standards.

---

## Deployment

- **Platform:** Render (Web Service)  
- **Framework:** Dash (Flask-based)  

**Start command:**
python app.py

yaml
Copy code

---

## Local Setup

git clone https://github.com/hamidakhtar27/statistical-arbitrage-platform.git
cd statistical-arbitrage-platform

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python app.py

arduino
Copy code

Then open:

http://127.0.0.1:8050

yaml
Copy code

---

## Limitations & Extensions

**Current limitations:**

- Simplified transaction cost modeling  
- Static universe of predefined pairs  
- No leverage or capital constraints  

**Planned extensions:**

- Kalman filter–based dynamic hedge ratios  
- Automated pair discovery  
- ML-based regime detection  
- Intraday and higher-frequency extensions  

---

## Why This Project Matters

This project demonstrates:

- Quantitative finance fundamentals  
- Statistical modeling and hypothesis testing  
- Clean, modular software architecture  
- Deployment and engineering maturity  
- Research-to-production thinking  

It is intentionally designed to be **interview-explainable**, **academically defensible**, and **industry-relevant**.

---

## Author

**Mohd Hamid Akhtar Khan**  
Final-year B.Tech (Computer Science & Engineering)  
Aspiring Quantitative Researcher / Trader  

GitHub: https://github.com/hamidakhtar27
If you want next, I can:

Convert this into resume bullets (elite quant wording)

Prepare a “walk me through this project” interview answer

Plan Project #2 to complement this perfectly











