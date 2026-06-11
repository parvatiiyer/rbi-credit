import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="India's Credit Decade",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0f0f0f; }
    .main  { background-color: #0f0f0f; }
    .metric-card {
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 18px 22px;
        margin: 4px 0;
    }
    .metric-value { font-size: 30px; font-weight: 700; color: #2a9d8f; margin: 4px 0; }
    .metric-label { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-delta-pos { font-size: 12px; color: #2a9d8f; margin-top: 4px; }
    .metric-delta-neg { font-size: 12px; color: #e63946; margin-top: 4px; }
    .chapter-header {
        background: linear-gradient(90deg, #1a1a1a, #0f0f0f);
        border-left: 3px solid #2a9d8f;
        padding: 10px 16px;
        margin: 20px 0 10px 0;
        border-radius: 0 6px 6px 0;
    }
    h1, h2, h3, h4 { color: white !important; }
    p, li { color: #ccc; }
    div[data-testid="stSidebarContent"] { background-color: #111 !important; }
    .stSlider label { color: #aaa !important; }
    .stSelectbox label { color: #aaa !important; }
</style>
""", unsafe_allow_html=True)

C = {
    "teal":   "#2a9d8f",
    "red":    "#e63946",
    "blue":   "#457b9d",
    "orange": "#f4a261",
    "yellow": "#e9c46a",
    "grey":   "#888888",
    "bg":     "#0f0f0f",
    "card":   "#1a1a1a",
    "grid":   "#2a2a2a",
}

BASE_LAYOUT = dict(
    paper_bgcolor=C["bg"],
    plot_bgcolor=C["card"],
    font=dict(color="white", family="Inter, Arial, sans-serif", size=12),
    margin=dict(l=55, r=25, t=50, b=50),
    legend=dict(bgcolor=C["card"], bordercolor="#333", borderwidth=1,
                font=dict(color="white", size=11)),
    xaxis=dict(gridcolor=C["grid"], zerolinecolor=C["grid"],
               color="white", showgrid=True),
    yaxis=dict(gridcolor=C["grid"], zerolinecolor=C["grid"],
               color="white", showgrid=True),
)

# ─────────────────────────────────────────────────────────────
# LOAD
# ─────────────────────────────────────────────────────────────

@st.cache_data
def load():
    m  = pd.read_csv("../data/processed/credit_dependency_master.csv")
    dg = pd.read_csv("../data/raw/digital_credit.csv")
    return m, dg

master, digital = load()

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🏦 India's Credit Decade")
    st.markdown("*How a nation learned to borrow (2005–2024)*")
    st.markdown("---")

    yr = st.slider("Year Range", 2005, 2024, (2005, 2024))

    st.markdown("---")
    st.markdown("### 📖 Story Chapters")
    st.markdown("""
- **Ch 1** — The Shift (2005–2014)
- **Ch 2** — The Explosion (2015–2020)
- **Ch 3** — COVID Stress Test (2020–2022)
- **Ch 4** — The New Normal (2022–2024)
    """)

    st.markdown("---")
    st.markdown("### 📊 Data Sources")
    st.markdown("""
- RBI Annual Reports
- RBI Financial Stability Reports
- RBI Payment System Reports
- World Bank Open Data
- MOSPI Wage Data
    """)

    st.markdown("---")
    st.markdown("### ⚡ Key Events")
    st.markdown("""
- 📉 **2008** Global Financial Crisis
- 📱 **2016** UPI Launch
- 🦠 **2020** COVID-19 Pandemic
- 🔺 **2022** RBI Rate Hike Cycle
    """)

f  = master[(master["year"] >= yr[0]) & (master["year"] <= yr[1])].copy()
dg = digital[(digital["year"] >= yr[0]) & (digital["year"] <= yr[1])].copy()

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────

st.markdown("# 🏦 India's Credit Decade")
st.markdown(
    f"*How Indian households went from savers to borrowers — "
    f"RBI Data Analysis {yr[0]}–{yr[1]}*"
)
st.markdown("---")

# ─────────────────────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────────────────────

def kpi_card(col, label, value, suffix="", delta=None, invert=False):
    """invert=True means up is bad (e.g. NPA, debt)"""
    delta_html = ""
    if delta is not None:
        pos = delta > 0
        good = pos if not invert else not pos
        cls  = "metric-delta-pos" if good else "metric-delta-neg"
        arrow = "▲" if pos else "▼"
        delta_html = f'<div class="{cls}">{arrow} {abs(delta):.2f}{suffix} vs prev yr</div>'
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}{suffix}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

latest = f.iloc[-1]
prev   = f.iloc[-2] if len(f) > 1 else latest

c1,c2,c3,c4,c5,c6 = st.columns(6)
kpi_card(c1, "Household Debt / GDP",   f"{latest['household_debt_gdp']:.1f}",  "%",
         latest["household_debt_gdp"] - prev["household_debt_gdp"], invert=True)
kpi_card(c2, "Retail Credit Growth",   f"{latest['retail_credit_growth']:.1f}", "%",
         latest["retail_credit_growth"] - prev["retail_credit_growth"])
kpi_card(c3, "Credit-to-GDP",          f"{latest['credit_to_gdp']:.1f}",       "%",
         latest["credit_to_gdp"] - prev["credit_to_gdp"], invert=True)
kpi_card(c4, "Household Savings Rate", f"{latest['household_savings_rate']:.1f}","%",
         latest["household_savings_rate"] - prev["household_savings_rate"])
kpi_card(c5, "Credit−Wage Gap",        f"{latest['credit_wage_gap']:.1f}",     "pp",
         latest["credit_wage_gap"] - prev["credit_wage_gap"], invert=True)
kpi_card(c6, "Affordability Stress",   f"{latest['affordability_stress']:.2f}", "x",
         latest["affordability_stress"] - prev["affordability_stress"], invert=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CHAPTER 1 — THE CORE DEPENDENCY STORY
# ─────────────────────────────────────────────────────────────

st.markdown('<div class="chapter-header"><h3 style="margin:0">📈 Chapter 1 — The Dependency Story</h3></div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Household debt vs savings — the scissors chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=f["year"], y=f["household_debt_gdp"],
        name="Household Debt / GDP %",
        line=dict(color=C["red"], width=3),
        fill="tozeroy", fillcolor="rgba(230,57,70,0.08)",
        mode="lines+markers", marker=dict(size=6)
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=f["year"], y=f["household_savings_rate"],
        name="Household Savings Rate %",
        line=dict(color=C["teal"], width=3),
        fill="tozeroy", fillcolor="rgba(42,157,143,0.08)",
        mode="lines+markers", marker=dict(size=6)
    ), secondary_y=True)

    # COVID band
    fig.add_vrect(x0=2019.5, x1=2021.5, fillcolor=C["red"],
                  opacity=0.06, annotation_text="COVID",
                  annotation_font_color=C["red"])

    fig.update_layout(
        title="The Scissors Effect — Debt Rising, Savings Falling",
        **BASE_LAYOUT
    )
    fig.update_yaxes(title_text="Household Debt / GDP %",
                     secondary_y=False, gridcolor=C["grid"], color="white")
    fig.update_yaxes(title_text="Household Savings Rate %",
                     secondary_y=True,  gridcolor=C["grid"], color="white")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("🔑 Key insight: As Indians borrowed more, they saved less — "
               "a structural shift in financial behaviour post-2015.")

with col2:
    # Credit-to-GDP over time
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=f["year"], y=f["credit_to_gdp"],
        name="Credit to GDP %",
        marker=dict(
            color=f["credit_to_gdp"],
            colorscale=[[0, C["blue"]], [0.5, C["teal"]], [1, C["orange"]]],
            showscale=True,
            colorbar=dict(
                title=dict(
                    text="%",
                    font=dict(color="white")
                ),
                tickfont=dict(color="white")
            )
        )
    ))
    fig2.add_hline(y=50, line_dash="dot", line_color=C["grey"],
                   annotation_text="50% threshold",
                   annotation_font_color=C["grey"])
    fig2.update_layout(
        title="Private Credit to GDP — Crossing the 50% Threshold",
        **BASE_LAYOUT
    )
    fig2.update_yaxes(title_text="Credit / GDP %")
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("🔑 Key insight: India crossed 50% credit-to-GDP in 2012 and "
               "spiked to 56% during COVID as GDP fell but credit held.")

# ─────────────────────────────────────────────────────────────
# CHAPTER 2 — WHAT ARE INDIANS BORROWING FOR
# ─────────────────────────────────────────────────────────────

st.markdown('<div class="chapter-header"><h3 style="margin:0">💳 Chapter 2 — What Are Indians Borrowing For?</h3></div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Retail credit growth by segment — line chart
    segments = [
        ("home",         "Home Loans",      C["teal"]),
        ("personal",     "Personal Loans",  C["orange"]),
        ("credit_card",  "Credit Cards",    C["red"]),
        ("auto",         "Auto Loans",      C["blue"]),
        ("education",    "Education",       C["yellow"]),
        ("gold",         "Gold Loans",      C["grey"]),
    ]
    fig3 = go.Figure()
    for col_name, label, color in segments:
        fig3.add_trace(go.Scatter(
            x=f["year"], y=f[col_name],
            name=label,
            line=dict(color=color, width=2),
            mode="lines+markers", marker=dict(size=5)
        ))
    fig3.add_hline(y=0, line_color="white", line_width=0.5)
    fig3.add_vrect(x0=2019.5, x1=2021.5, fillcolor=C["red"],
                   opacity=0.06, annotation_text="COVID",
                   annotation_font_color=C["red"])
    layout = BASE_LAYOUT.copy()

    layout["legend"] = {
        **BASE_LAYOUT["legend"],
        "orientation": "h",
        "x": 0,
        "y": -0.25
    }

    fig3.update_layout(
        title="Retail Credit Growth by Segment (YoY %)",
        **layout
    )
    fig3.update_yaxes(title_text="YoY Growth %")
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("🔑 Key insight: Personal loans and credit cards grew fastest "
               "post-2016 — consumption credit outpacing asset-backed credit.")

with col2:
    # Outstanding credit index (2005=100) — stacked area
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=f["year"], y=f["personal_outstanding"],
        name="Personal Loans", fill="tozeroy",
        line=dict(color=C["orange"], width=2),
        fillcolor="rgba(244,162,97,0.3)"
    ))
    fig4.add_trace(go.Scatter(
        x=f["year"], y=f["home_outstanding"],
        name="Home Loans", fill="tonexty",
        line=dict(color=C["teal"], width=2),
        fillcolor="rgba(42,157,143,0.3)"
    ))
    fig4.add_trace(go.Scatter(
        x=f["year"], y=f["creditcard_outstanding"],
        name="Credit Cards", fill="tonexty",
        line=dict(color=C["red"], width=2),
        fillcolor="rgba(230,57,70,0.3)"
    ))
    fig4.update_layout(
        title="Outstanding Credit Index (2005 = 100)",
        **BASE_LAYOUT
    )
    fig4.update_yaxes(title_text="Index (2005=100)")
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("🔑 Key insight: Personal loan outstanding grew 31x since 2005 "
               "vs 18x for home loans — India is borrowing to consume, not just to own.")

# ─────────────────────────────────────────────────────────────
# CHAPTER 3 — CAN INDIANS AFFORD THIS?
# ─────────────────────────────────────────────────────────────

st.markdown('<div class="chapter-header"><h3 style="margin:0">⚠️ Chapter 3 — Can Indians Afford What They\'re Borrowing?</h3></div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Credit growth vs wage growth — the affordability gap
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=f["year"], y=f["retail_credit_growth"],
        name="Retail Credit Growth %",
        marker_color=C["red"], opacity=0.8
    ))
    fig5.add_trace(go.Bar(
        x=f["year"], y=f["avg_wage_growth"],
        name="Average Wage Growth %",
        marker_color=C["teal"], opacity=0.8
    ))
    fig5.add_trace(go.Scatter(
        x=f["year"], y=f["credit_wage_gap"],
        name="Gap (Credit − Wages)",
        line=dict(color=C["yellow"], width=2.5, dash="dash"),
        mode="lines+markers", marker=dict(size=6)
    ))
    fig5.add_hline(y=0, line_color="white", line_width=0.5)
    layout = BASE_LAYOUT.copy()

    layout["legend"] = {
        **BASE_LAYOUT["legend"],
        "orientation": "h",
        "x": 0,
        "y": -0.25
    }

    fig5.update_layout(
        title="Credit Growth vs Wage Growth – The Affordability Gap",
        **layout
    )
    fig5.update_yaxes(title_text="%")
    st.plotly_chart(fig5, use_container_width=True)
    st.caption("🔑 Key insight: Since 2015, credit has grown faster than wages "
               "every single year except 2020 — borrowers are taking on more "
               "debt than their income growth can comfortably support.")

with col2:
    # Retail NPA by segment
    npa_df = f.dropna(subset=["home_npa"])
    fig6 = go.Figure()
    npa_segments = [
        ("creditcard_npa", "Credit Cards", C["red"]),
        ("education_npa",  "Education",    C["orange"]),
        ("personal_npa",   "Personal",     C["yellow"]),
        ("auto_npa",       "Auto",         C["blue"]),
        ("home_npa",       "Home Loans",   C["teal"]),
    ]
    for col_name, label, color in npa_segments:
        fig6.add_trace(go.Scatter(
            x=npa_df["year"], y=npa_df[col_name],
            name=label,
            line=dict(color=color, width=2),
            mode="lines+markers", marker=dict(size=6)
        ))
    fig6.add_vrect(x0=2019.5, x1=2021.5, fillcolor=C["red"],
                   opacity=0.08, annotation_text="COVID Peak",
                   annotation_font_color=C["red"])
    fig6.update_layout(
        title="Retail NPA by Segment % (2015–2024)",
        **BASE_LAYOUT
    )
    fig6.update_yaxes(title_text="NPA %")
    st.plotly_chart(fig6, use_container_width=True)
    st.caption("🔑 Key insight: Credit card and education NPAs peaked during "
               "COVID at 6.5% and 8.8% respectively — unsecured lending is "
               "most vulnerable to income shocks.")

# Affordability stress full width
fig7 = go.Figure()
fig7.add_trace(go.Bar(
    x=f["year"],
    y=f["affordability_stress"],
    marker=dict(
        color=f["affordability_stress"],
        colorscale=[[0, C["teal"]], [0.5, C["yellow"]], [1, C["red"]]],
        showscale=True,
        colorbar=dict(
            title=dict(
                text="Stress\nIndex",
                font=dict(color="white")
            ),
            tickfont=dict(color="white")
        )
    ),
    name="Affordability Stress Index"
))
fig7.update_layout(
    title="Affordability Stress Index = Household Debt/GDP ÷ Savings Rate "
          "(Higher = More Stressed)",
    **BASE_LAYOUT,
    height=300
)
fig7.update_yaxes(title_text="Stress Index")
st.plotly_chart(fig7, use_container_width=True)
st.caption("🔑 Key insight: The affordability stress index has risen 43% since "
           "2015 — Indians are carrying more debt relative to their savings buffer.")

# ─────────────────────────────────────────────────────────────
# CHAPTER 4 — THE DIGITAL CREDIT EXPLOSION
# ─────────────────────────────────────────────────────────────

st.markdown('<div class="chapter-header"><h3 style="margin:0">📱 Chapter 4 — The Digital Credit Explosion</h3></div>',
            unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    fig8 = make_subplots(specs=[[{"secondary_y": True}]])
    fig8.add_trace(go.Bar(
        x=dg["year"], y=dg["cards_outstanding_mn"],
        name="Cards Outstanding (Mn)",
        marker_color=C["teal"], opacity=0.8
    ), secondary_y=False)
    fig8.add_trace(go.Scatter(
        x=dg["year"], y=dg["card_spends_bn_inr"],
        name="Card Spends (₹ Bn)",
        line=dict(color=C["orange"], width=2.5),
        mode="lines+markers"
    ), secondary_y=True)
    layout = BASE_LAYOUT.copy()

    layout["legend"] = {
        **BASE_LAYOUT["legend"],
        "orientation": "h",
        "x": 0,
        "y": -0.25
    }

    fig8.update_layout(
        title="Some Title",
        **layout
    )
    fig8.update_yaxes(title_text="Cards (Mn)",    secondary_y=False,
                      gridcolor=C["grid"], color="white")
    fig8.update_yaxes(title_text="Spends (₹ Bn)", secondary_y=True,
                      gridcolor=C["grid"], color="white")
    st.plotly_chart(fig8, use_container_width=True)

with col2:
    fig9 = make_subplots(specs=[[{"secondary_y": True}]])
    fig9.add_trace(go.Bar(
        x=dg["year"], y=dg["upi_transactions_bn"],
        name="UPI Transactions (Bn)",
        marker_color=C["blue"], opacity=0.8
    ), secondary_y=False)
    fig9.add_trace(go.Scatter(
        x=dg["year"], y=dg["bnpl_users_mn"],
        name="BNPL Users (Mn)",
        line=dict(color=C["red"], width=2.5),
        mode="lines+markers"
    ), secondary_y=True)
    layout = BASE_LAYOUT.copy()

    layout["legend"] = {
        **BASE_LAYOUT["legend"],
        "orientation": "h",
        "x": 0,
        "y": -0.25
    }

    fig9.update_layout(
        title="Your Chart Title",
        **layout
    )
    fig9.update_yaxes(title_text="UPI (Bn txns)", secondary_y=False,
                      gridcolor=C["grid"], color="white")
    fig9.update_yaxes(title_text="BNPL Users (Mn)", secondary_y=True,
                      gridcolor=C["grid"], color="white")
    st.plotly_chart(fig9, use_container_width=True)

with col3:
    fig10 = go.Figure()
    fig10.add_trace(go.Bar(
        x=dg["year"], y=dg["digital_lending_bn"],
        marker=dict(
            color=dg["digital_lending_bn"],
            colorscale=[[0, C["blue"]], [1, C["red"]]],
            showscale=False
        ),
        name="Digital Lending (₹ Bn)"
    ))
    layout = BASE_LAYOUT.copy()

    layout["legend"] = {
        **BASE_LAYOUT["legend"],
        "orientation": "h",
        "x": 0,
        "y": -0.25
    }

    fig10.update_layout(
        title="Digital Lending (₹ Bn)",
        **layout
    )
    fig10.update_yaxes(title_text="₹ Billion")
    st.plotly_chart(fig10, use_container_width=True)

st.caption("🔑 Key insight: Digital lending grew 100x from ₹150 Bn (2015) to "
           "₹15,000 Bn (2024). UPI, launched in 2016, normalised digital "
           "transactions and created the infrastructure for BNPL to explode.")

# ─────────────────────────────────────────────────────────────
# CHAPTER 5 — MACRO CONTEXT
# ─────────────────────────────────────────────────────────────

st.markdown('<div class="chapter-header"><h3 style="margin:0">🏛️ Chapter 5 — The Macro Environment That Enabled It</h3></div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig11 = make_subplots(specs=[[{"secondary_y": True}]])
    fig11.add_trace(go.Scatter(
        x=f["year"], y=f["repo_rate"],
        name="Repo Rate %",
        line=dict(color=C["orange"], width=2.5),
        mode="lines+markers", marker=dict(size=6)
    ), secondary_y=False)
    fig11.add_trace(go.Scatter(
        x=f["year"], y=f["cpi_inflation"],
        name="CPI Inflation %",
        line=dict(color=C["red"], width=2, dash="dash"),
        mode="lines"
    ), secondary_y=False)
    fig11.add_trace(go.Bar(
        x=f["year"], y=f["retail_credit_growth"],
        name="Retail Credit Growth %",
        marker_color=C["teal"], opacity=0.4
    ), secondary_y=True)
    fig11.add_hline(y=4.0, line_dash="dot", line_color=C["grey"],
                    annotation_text="RBI 4% target")
    layout = BASE_LAYOUT.copy()

    layout["legend"] = {
        **BASE_LAYOUT["legend"],
        "orientation": "h",
        "x": 0,
        "y": -0.25
    }

    fig11.update_layout(
        title="Repo Rate & Inflation vs Credit Growth",
        **layout
    )
    fig11.update_yaxes(title_text="Rate / Inflation %",    secondary_y=False,
                       gridcolor=C["grid"], color="white")
    fig11.update_yaxes(title_text="Credit Growth %", secondary_y=True,
                       gridcolor=C["grid"], color="white")
    st.plotly_chart(fig11, use_container_width=True)
    st.caption("🔑 Key insight: The 2017–2021 low interest rate cycle (repo at "
               "4%) directly enabled the credit explosion — cheap money made "
               "borrowing attractive for a generation new to formal credit.")

with col2:
    # Correlation heatmap
    corr_cols = ["retail_credit_growth", "household_debt_gdp",
                 "household_savings_rate", "avg_wage_growth",
                 "repo_rate", "cpi_inflation", "gdp_growth",
                 "credit_to_gdp"]
    corr_labels = ["Credit Growth", "HH Debt/GDP", "Savings Rate",
                   "Wage Growth", "Repo Rate", "Inflation",
                   "GDP Growth", "Credit/GDP"]
    corr_matrix = f[corr_cols].corr().round(2)

    fig12 = go.Figure(go.Heatmap(
        z=corr_matrix.values,
        x=corr_labels, y=corr_labels,
        colorscale="RdBu", zmid=0,
        text=corr_matrix.values,
        texttemplate="%{text}",
        textfont=dict(size=10),
        colorbar=dict(
        title=dict(
            text="r",
            font=dict(color="white")
        ),
        tickfont=dict(color="white")
    )
    ))
    layout = BASE_LAYOUT.copy()

    layout["xaxis"] = {
        **BASE_LAYOUT["xaxis"],
        "tickfont": dict(size=9),
        "color": "white",
        "tickangle": 45,
        "gridcolor": C["grid"]
    }

    layout["yaxis"] = {
        **BASE_LAYOUT["yaxis"],
        "tickfont": dict(size=9),
        "color": "white",
        "gridcolor": C["grid"]
    }

    fig12.update_layout(
        title="Correlation Matrix — Credit Dependency Variables",
        **layout
    )
    st.plotly_chart(fig12, use_container_width=True)
    st.caption("🔑 Key insight: Savings rate and household debt are strongly "
               "negatively correlated (-0.97) — the most direct evidence of "
               "the savings-to-borrowing behavioural shift.")

# ─────────────────────────────────────────────────────────────
# SUMMARY FINDINGS
# ─────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("## 📋 Summary — India's Credit Dependency in 5 Numbers")

s1, s2, s3, s4, s5 = st.columns(5)
kpi_card(s1, "Household Debt Rise",   "2.8x",  "",  None)
kpi_card(s2, "Personal Loan Growth",  "31x",   "",  None)
kpi_card(s3, "Savings Rate Drop",     "−7pp",  "",  None)
kpi_card(s4, "Digital Lending Jump",  "100x",  "",  None)
kpi_card(s5, "Credit Cards Issued",   "5.3x",  "",  None)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
**The central argument:** India's relationship with credit fundamentally changed between 2015 and 2024.
A generation that grew up in a savings-first culture discovered EMIs, credit cards, and BNPL apps.
The infrastructure (UPI, Aadhaar, digital KYC) made it frictionless.
The question for Indian banks is no longer *how to grow credit* — it is *whether this pace is sustainable*
given that real wage growth has consistently lagged credit growth since 2016.
""")

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style='color:#555; font-size:11px; text-align:center;'>
Data: RBI Annual Reports · RBI Financial Stability Reports ·
RBI Payment System Reports · World Bank Open Data · MOSPI |
Built with Python · Streamlit · Plotly
</div>
""", unsafe_allow_html=True)