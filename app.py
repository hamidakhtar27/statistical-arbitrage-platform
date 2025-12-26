import os
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash import Dash, dcc, html, Input, Output
from dash.exceptions import PreventUpdate

from src.research.cointegration import engle_granger_test
from src.research.spread import compute_spread
from src.strategy.signals import generate_signals
from src.strategy.portfolio import backtest_portfolio
from src.analytics.performance import compute_performance_metrics

# ================================
# DASH APP
# ================================
app = Dash(__name__)
server = app.server

# ================================
# LOCAL DATA
# ================================
DATA_DIR = Path("data")

PAIRS = {
    "INFY_TCS": DATA_DIR / "INFY_TCS.csv",
    "HDFCBANK_ICICI": DATA_DIR / "HDFCBANK_ICICI.csv",
    "RELIANCE_ONGC": DATA_DIR / "RELIANCE_ONGC.csv",
}

PRICE_DATA = {}

for key, path in PAIRS.items():
    if not path.exists():
        raise RuntimeError(f"Missing data file: {path}")

    df = pd.read_csv(path, index_col=0, parse_dates=True)

    if df.empty:
        raise RuntimeError(f"Empty data file: {path}")

    PRICE_DATA[key] = df.dropna()

# ================================
# HEDGE RATIO EXTRACTOR
# ================================
def extract_hedge_ratio(result):
    if isinstance(result, dict) and "hedge_ratio" in result:
        return float(result["hedge_ratio"])
    if isinstance(result, (tuple, list)):
        return float(result[0])
    if hasattr(result, "hedge_ratio"):
        return float(result.hedge_ratio)
    raise ValueError("Cannot extract hedge ratio")

# ================================
# LAYOUT
# ================================
app.layout = html.Div(
    style={
        "backgroundColor": "#0b1220",
        "minHeight": "100vh",
        "padding": "20px",
        "color": "#e5e7eb",
        "fontFamily": "Arial"
    },
    children=[

        html.H2("Statistical Arbitrage Research Platform"),

        html.Div(style={"display": "flex", "gap": "20px"}, children=[

            # ===== SIDEBAR =====
            html.Div(
                style={
                    "width": "22%",
                    "backgroundColor": "#0f172a",
                    "padding": "20px",
                    "borderRadius": "10px"
                },
                children=[
                    html.Label("Asset Pair"),
                    dcc.Dropdown(
                        id="pair",
                        options=[
                            {"label": k.replace("_", " – "), "value": k}
                            for k in PAIRS
                        ],
                        value="INFY_TCS",
                        clearable=False
                    ),

                    html.Br(),
                    html.Label("Entry Z"),
                    dcc.Slider(1.5, 3.0, 0.1, value=2.0, id="entry_z"),

                    html.Br(),
                    html.Label("Exit Z"),
                    dcc.Slider(0.2, 1.0, 0.1, value=0.5, id="exit_z"),

                    html.Br(),
                    html.Label("Rolling Window"),
                    dcc.Slider(30, 120, 10, value=60, id="window"),

                    html.Hr(),
                    html.Div(id="metrics")
                ]
            ),

            # ===== MAIN =====
            html.Div(style={"width": "78%"}, children=[
                dcc.Tabs([
                    dcc.Tab(label="Spread & Z-Score", children=[dcc.Graph(id="spread_graph")]),
                    dcc.Tab(label="Performance", children=[dcc.Graph(id="equity_graph")])
                ])
            ])
        ])
    ]
)

# ================================
# CALLBACK
# ================================
@app.callback(
    Output("spread_graph", "figure"),
    Output("equity_graph", "figure"),
    Output("metrics", "children"),
    Input("pair", "value"),
    Input("entry_z", "value"),
    Input("exit_z", "value"),
    Input("window", "value"),
)
def update_dashboard(pair, entry_z, exit_z, window):

    if pair not in PRICE_DATA:
        raise PreventUpdate

    prices = PRICE_DATA[pair]

    if window >= len(prices):
        raise PreventUpdate

    y, x = prices.iloc[:, 0], prices.iloc[:, 1]

    result = engle_granger_test(y, x)
    hedge_ratio = extract_hedge_ratio(result)

    spread = compute_spread(y, x, hedge_ratio)
    zscore = (spread - spread.rolling(window).mean()) / spread.rolling(window).std()
    zscore = zscore.dropna()

    signals = generate_signals(zscore, entry_z, exit_z)

    prices = prices.loc[zscore.index]
    spread = spread.loc[zscore.index]
    signals = signals.loc[zscore.index]

    portfolio = backtest_portfolio(prices, spread, signals)

    metrics = compute_performance_metrics(
        portfolio["equity_curve"],
        portfolio["pnl"]
    )

    # ===== Spread & Z-Score =====
    f1 = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        subplot_titles=("Cointegrated Spread", "Z-Score")
    )

    f1.add_trace(go.Scatter(x=spread.index, y=spread, name="Spread", line=dict(color="#60a5fa")), 1, 1)
    f1.add_trace(go.Scatter(x=zscore.index, y=zscore, name="Z-Score", line=dict(color="#f97316")), 2, 1)

    for lvl in [entry_z, -entry_z]:
        f1.add_hline(y=lvl, row=2, line_dash="dot", line_color="#64748b")

    f1.add_hline(y=0, row=2, line_color="#94a3b8")

    f1.update_layout(template="plotly_dark", height=700)

    # ===== Performance =====
    f2 = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        subplot_titles=("Equity Curve", "Drawdown")
    )

    f2.add_trace(go.Scatter(x=portfolio.index, y=portfolio["equity_curve"],
                            name="Equity", line=dict(color="#22c55e")), 1, 1)

    f2.add_trace(go.Scatter(x=portfolio.index, y=portfolio["drawdown"],
                            name="Drawdown", fill="tozeroy",
                            line=dict(color="#fb7185")), 2, 1)

    f2.update_layout(template="plotly_dark", height=650)

    metrics_block = [
        html.P(f"Hedge Ratio: {hedge_ratio:.3f}"),
        html.P(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}"),
        html.P(f"Max Drawdown: {metrics['Max Drawdown']:.2%}"),
        html.P(f"Total Return: {metrics['Total Return']:.2%}")
    ]

    return f1, f2, metrics_block

# ================================
# RUN
# ================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
