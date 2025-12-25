import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ================================
# CORE LOGIC IMPORTS
# ================================
from src.data.loader import load_price_data
from src.research.cointegration import engle_granger_test
from src.research.spread import compute_spread
from src.strategy.signals import compute_zscore
from src.strategy.portfolio import generate_positions
from src.backtest.costs import apply_transaction_costs
from src.backtest.engine import backtest_spread_strategy
from src.analytics.performance import compute_performance_metrics

# ================================
# APP
# ================================
app = dash.Dash(__name__)
app.title = "Statistical Arbitrage Research Platform"

# ================================
# COLOR SYSTEM (REFINED)
# ================================
BG = "#0b1220"
CARD = "#0f172a"
TEXT = "#e5e7eb"

SPREAD = "#60a5fa"
LONG = "#22c55e"
SHORT = "#ef4444"

ZSCORE = "#9ca3af"
BAND = "#475569"
ZERO = "#64748b"

EQUITY = "#22c55e"
DRAWDOWN = "#fb7185"

GRID = "#1e293b"
CAPTION = "#94a3b8"

# ================================
# PIPELINE
# ================================
def run_pipeline(a, b, entry_z, exit_z, window):
    prices = load_price_data([a, b])
    y, x = prices[a], prices[b]

    beta = engle_granger_test(y, x)["hedge_ratio"]
    spread = compute_spread(y, x, beta)
    z = compute_zscore(spread, window)
    pos = generate_positions(z, entry_z, exit_z)

    costs = apply_transaction_costs(pos)
    res = backtest_spread_strategy(spread, pos, costs)
    metrics = compute_performance_metrics(res["equity"], res["net_pnl"])

    equity = res["equity"]
    drawdown = equity - equity.cummax()

    pc = pos.diff()
    long_e = spread[pc == 1]
    short_e = spread[pc == -1]
    exits = spread[(pc.abs() == 1) & (pos == 0)]

    return beta, spread, z, equity, drawdown, metrics, long_e, short_e, exits

# ================================
# LAYOUT
# ================================
app.layout = html.Div(
    style={"backgroundColor": BG, "height": "100vh", "padding": "20px"},
    children=[

        html.H2(
            "Statistical Arbitrage Research Platform",
            style={"color": TEXT, "marginBottom": "20px"}
        ),

        html.Div(
            style={"display": "flex", "gap": "20px"},

            children=[

                # ===== LEFT SIDEBAR =====
                html.Div(
                    style={
                        "width": "22%",
                        "backgroundColor": CARD,
                        "padding": "20px",
                        "borderRadius": "12px"
                    },
                    children=[

                        html.Label("Asset Pair", style={"color": TEXT}),
                        dcc.Dropdown(
                            id="pair",
                            options=[
                                {"label": "INFY – TCS", "value": "INFY.NS|TCS.NS"},
                                {"label": "HDFCBANK – ICICIBANK", "value": "HDFCBANK.NS|ICICIBANK.NS"},
                                {"label": "RELIANCE – ONGC", "value": "RELIANCE.NS|ONGC.NS"},
                                {"label": "SBIN – AXISBANK", "value": "SBIN.NS|AXISBANK.NS"},
                                {"label": "LT – ULTRACEMCO", "value": "LT.NS|ULTRACEMCO.NS"},
                            ],
                            value="INFY.NS|TCS.NS",
                            clearable=False
                        ),

                        html.Br(),

                        html.Label("Entry Z", style={"color": TEXT}),
                        dcc.Slider(1.5, 3.0, 0.1, value=2.0, id="entry"),

                        html.Br(),

                        html.Label("Exit Z", style={"color": TEXT}),
                        dcc.Slider(0.2, 1.0, 0.1, value=0.5, id="exit"),

                        html.Br(),

                        html.Label("Rolling Window", style={"color": TEXT}),
                        dcc.Slider(30, 120, 10, value=60, id="window"),

                        html.Hr(style={"borderColor": GRID}),

                        html.Div(id="metrics", style={"color": TEXT})
                    ]
                ),

                # ===== MAIN CONTENT =====
                html.Div(
                    style={"width": "78%"},
                    children=[

                        dcc.Tabs([

                            dcc.Tab(
                                label="Spread & Z-Score",
                                children=[
                                    dcc.Graph(id="spread-graph"),
                                    html.P(
                                        "Cointegrated spread with long/short trade markers (top) "
                                        "and corresponding Z-score with ±2 entry thresholds (bottom).",
                                        style={"color": CAPTION, "fontSize": "13px", "marginTop": "6px"}
                                    )
                                ]
                            ),

                            dcc.Tab(
                                label="Performance",
                                children=[
                                    dcc.Graph(id="equity-graph"),
                                    html.P(
                                        "Cumulative equity curve (top) and drawdown relative to rolling peak (bottom).",
                                        style={"color": CAPTION, "fontSize": "13px", "marginTop": "6px"}
                                    )
                                ]
                            )

                        ])
                    ]
                )
            ]
        )
    ]
)

# ================================
# CALLBACK
# ================================
@app.callback(
    Output("spread-graph", "figure"),
    Output("equity-graph", "figure"),
    Output("metrics", "children"),
    Input("pair", "value"),
    Input("entry", "value"),
    Input("exit", "value"),
    Input("window", "value"),
)
def update(pair, entry, exit, window):
    a, b = pair.split("|")
    beta, spread, z, equity, dd, m, L, S, E = run_pipeline(a, b, entry, exit, window)

    # ---------- SPREAD + Z-SCORE ----------
    f1 = make_subplots(rows=2, cols=1, shared_xaxes=True)

    f1.add_trace(go.Scatter(x=spread.index, y=spread,
                            line=dict(color=SPREAD, width=1.6),
                            name="Spread"), 1, 1)

    f1.add_trace(go.Scatter(x=L.index, y=L,
                            mode="markers",
                            marker=dict(color=LONG, symbol="triangle-up", size=8),
                            name="Long"), 1, 1)

    f1.add_trace(go.Scatter(x=S.index, y=S,
                            mode="markers",
                            marker=dict(color=SHORT, symbol="triangle-down", size=8),
                            name="Short"), 1, 1)

    f1.add_trace(go.Scatter(x=z.index, y=z,
                            line=dict(color=ZSCORE, width=1.2),
                            name="Z-Score"), 2, 1)

    for lvl in [2, -2]:
        f1.add_hline(y=lvl, row=2,
                     line_dash="dot",
                     line_color=BAND,
                     line_width=1)

    f1.add_hline(y=0, row=2, line_color=ZERO, line_width=1)

    f1.update_layout(
        template="plotly_dark",
        height=720,
        plot_bgcolor=CARD,
        paper_bgcolor=CARD
    )

    f1.update_xaxes(gridcolor=GRID)
    f1.update_yaxes(gridcolor=GRID)

    # ---------- EQUITY + DRAWDOWN ----------
    f2 = make_subplots(rows=2, cols=1, shared_xaxes=True)

    f2.add_trace(go.Scatter(x=equity.index, y=equity,
                            line=dict(color=EQUITY, width=1.6),
                            name="Equity"), 1, 1)

    f2.add_trace(go.Scatter(x=dd.index, y=dd,
                            fill="tozeroy",
                            line=dict(color=DRAWDOWN, width=1.2),
                            name="Drawdown"), 2, 1)

    f2.update_layout(
        template="plotly_dark",
        height=640,
        plot_bgcolor=CARD,
        paper_bgcolor=CARD
    )

    f2.update_xaxes(gridcolor=GRID)
    f2.update_yaxes(gridcolor=GRID)

    metrics = [
        html.P(f"Hedge Ratio: {beta:.3f}"),
        html.P(f"Sharpe: {m['Sharpe Ratio']:.2f}"),
        html.P(f"Max DD: {m['Max Drawdown']:.2%}"),
        html.P(f"Return: {m['Total Return']:.2f}")
    ]

    return f1, f2, metrics

# ================================
# RUN
# ================================
if __name__ == "__main__":
    app.run(debug=True)
