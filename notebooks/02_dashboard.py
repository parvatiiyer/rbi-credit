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
    st.markdown("India's Credit Decade")
    st.markdown("*How a nation learned to borrow (2005–2024)*")
    st.markdown("---")

    yr = st.slider("Year Range", 2005, 2024, (2005, 2024))

    st.markdown("---")
    st.markdown("### The Story in Four Acts")
    st.markdown("""
**2005–2014 — The Foundation**
Home loans dominate. Credit cards are urban and elite.
Savings rate sits above 22%. Borrowing is a last resort, not a lifestyle.

**2015–2019 — The Shift**
Repo rate falls. Jan Dhan brings 400M people into banking.
UPI launches in 2016. Personal loans overtake home loans in growth rate.
A generation discovers the EMI.

**2020–2021 — The Stress Test**
COVID hits. Income falls, but credit doesn't — digital lenders fill the gap.
Credit card NPAs hit 6.5%. BNPL users double in 12 months.
Savings rate spikes briefly, then falls harder than before.

**2022–2024 — The New Normal**
RBI hikes 250bps. Credit growth barely slows.
Demand is now structural. The savings rate hits a historic low of 16.5%.
India is no longer a nation of savers.
    """)

    st.markdown("---")
    st.markdown("### Data Sources")
    st.markdown("""
- RBI Annual Reports
- RBI Financial Stability Reports
- RBI Payment System Reports
- World Bank Open Data API
- MOSPI Wage Data
    """)

f  = master[(master["year"] >= yr[0]) & (master["year"] <= yr[1])].copy()
dg = digital[(digital["year"] >= yr[0]) & (digital["year"] <= yr[1])].copy()

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────

st.markdown("# India's Credit Decade")
st.markdown(
    f"*How Indian households went from savers to borrowers — "
    f"RBI Data Analysis {yr[0]}–{yr[1]}*"
)
st.markdown("""
*This dashboard tracks the structural shift in Indian household finance over 20 years.
The central question: is India's credit growth a sign of rising prosperity —
or are households borrowing faster than they can afford to repay?*
""")
st.markdown("---")

# ─────────────────────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────────────────────

def kpi_card(col, label, value, suffix="", delta=None, invert=False):
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
kpi_card(c1, "Household Debt / GDP",   f"{latest['household_debt_gdp']:.1f}",   "%",
         latest["household_debt_gdp"]    - prev["household_debt_gdp"],    invert=True)
kpi_card(c2, "Retail Credit Growth",   f"{latest['retail_credit_growth']:.1f}", "%",
         latest["retail_credit_growth"] - prev["retail_credit_growth"])
kpi_card(c3, "Credit-to-GDP",          f"{latest['credit_to_gdp']:.1f}",        "%",
         latest["credit_to_gdp"]        - prev["credit_to_gdp"],         invert=True)
kpi_card(c4, "Household Savings Rate", f"{latest['household_savings_rate']:.1f}","%",
         latest["household_savings_rate"]- prev["household_savings_rate"])
kpi_card(c5, "Credit − Wage Gap",      f"{latest['credit_wage_gap']:.1f}",      "pp",
         latest["credit_wage_gap"]      - prev["credit_wage_gap"],        invert=True)
kpi_card(c6, "Affordability Stress",   f"{latest['affordability_stress']:.2f}", "x",
         latest["affordability_stress"] - prev["affordability_stress"],   invert=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# CHAPTER 1 — THE SCISSORS EFFECT
# ─────────────────────────────────────────────────────────────

st.markdown(
    '<div class="chapter-header"><h3 style="margin:0">'
    'The Scissors Effect — Debt Up, Savings Down, Every Year Since 2015'
    '</h3></div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
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
    fig.add_vrect(x0=2019.5, x1=2021.5, fillcolor=C["red"],
                  opacity=0.06, annotation_text="COVID",
                  annotation_font_color=C["red"])
    fig.update_layout(
        title="Household Debt vs Savings Rate (2005–2024)",
        **BASE_LAYOUT
    )
    fig.update_yaxes(title_text="Household Debt / GDP %",
                     secondary_y=False, gridcolor=C["grid"], color="white")
    fig.update_yaxes(title_text="Household Savings Rate %",
                     secondary_y=True,  gridcolor=C["grid"], color="white")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Savings rate fell 7 percentage points between 2015 and 2024 — "
        "the steepest sustained decline in decades. "
        "The two lines crossed around 2018 and have diverged every year since. "
        "The open question: is this Indians growing more confident, "
        "or more stretched?"
    )

with col2:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=f["year"], y=f["credit_to_gdp"],
        name="Credit to GDP %",
        marker=dict(
            color=f["credit_to_gdp"],
            colorscale=[[0, C["blue"]], [0.5, C["teal"]], [1, C["orange"]]],
            showscale=True,
            colorbar=dict(
                title=dict(text="%", font=dict(color="white")),
                tickfont=dict(color="white")
            )
        )
    ))
    fig2.add_hline(y=50, line_dash="dot", line_color=C["grey"],
                   annotation_text="50% threshold",
                   annotation_font_color=C["grey"])
    fig2.update_layout(
        title="Private Sector Credit as % of GDP",
        **BASE_LAYOUT
    )
    fig2.update_yaxes(title_text="Credit / GDP %")
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "India crossed the 50% credit-to-GDP mark around 2012 and hit 56% "
        "during COVID — not because credit grew, but because GDP collapsed "
        "while banks kept lending. That distinction matters: "
        "it means Indian banks made an active choice to extend credit "
        "during an income shock."
    )

# ─────────────────────────────────────────────────────────────
# CHAPTER 2 — WHAT ARE INDIANS BORROWING FOR
# ─────────────────────────────────────────────────────────────

st.markdown(
    '<div class="chapter-header"><h3 style="margin:0">'
    'From Home Loans to Credit Cards — How Borrowing Changed Shape'
    '</h3></div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    segments = [
        ("home",        "Home Loans",     C["teal"]),
        ("personal",    "Personal Loans", C["orange"]),
        ("credit_card", "Credit Cards",   C["red"]),
        ("auto",        "Auto Loans",     C["blue"]),
        ("education",   "Education",      C["yellow"]),
        ("gold",        "Gold Loans",     C["grey"]),
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
    layout3 = BASE_LAYOUT.copy()
    layout3["legend"] = {**BASE_LAYOUT["legend"],
                         "orientation": "h", "x": 0, "y": -0.28}
    fig3.update_layout(title="Retail Credit Growth by Segment (YoY %)", **layout3)
    fig3.update_yaxes(title_text="YoY Growth %")
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        "Credit card growth hit 40% in 2007, crashed to -5% in 2009, "
        "then rebuilt steadily — peaking again at 32% in 2018. "
        "Personal loans tell a different story: they never really slowed down. "
        "Post-2016, consumption credit systematically outgrew every "
        "asset-backed category."
    )

with col2:
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
    st.caption(
        "In 2005 home loans and personal loans grew at roughly the same pace. "
        "By 2024 personal loan outstanding is 31x the 2005 base; "
        "home loans are 18x. "
        "The gap is not about housing demand slowing — "
        "it is about an entirely new category of borrowing emerging: "
        "consumption, lifestyle, and emergency credit."
    )

# ─────────────────────────────────────────────────────────────
# CHAPTER 3 — AFFORDABILITY
# ─────────────────────────────────────────────────────────────

st.markdown(
    '<div class="chapter-header"><h3 style="margin:0">'
    'The Affordability Question — Credit Growing 2x Faster Than Wages'
    '</h3></div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
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
    layout5 = BASE_LAYOUT.copy()
    layout5["legend"] = {**BASE_LAYOUT["legend"],
                         "orientation": "h", "x": 0, "y": -0.28}
    fig5.update_layout(
        title="Credit Growth vs Wage Growth — The Affordability Gap",
        barmode="group", **layout5
    )
    fig5.update_yaxes(title_text="%")
    st.plotly_chart(fig5, use_container_width=True)
    st.caption(
        "Credit has outgrown wages every year since 2016 except 2020 — "
        "and even in 2020 wages fell harder than credit slowed. "
        "The gap averaged 14 percentage points between 2018 and 2024. "
        "This is the number that should concern any retail lending analyst: "
        "borrowers are accumulating obligations faster than their "
        "income can service them."
    )

with col2:
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
        title="Retail NPA by Segment % — Where Stress Shows Up",
        **BASE_LAYOUT
    )
    fig6.update_yaxes(title_text="NPA %")
    st.plotly_chart(fig6, use_container_width=True)
    st.caption(
        "COVID was the stress test nobody planned for. "
        "Credit card NPAs hit 6.5%, education loans 8.8%. "
        "Home loans — secured, long-tenure — held at 2.8%. "
        "The recovery was fast, but the pattern is clear: "
        "the faster a segment grows, the harder it falls "
        "when incomes are disrupted."
    )

fig7 = go.Figure()
fig7.add_trace(go.Bar(
    x=f["year"],
    y=f["affordability_stress"],
    marker=dict(
        color=f["affordability_stress"],
        colorscale=[[0, C["teal"]], [0.5, C["yellow"]], [1, C["red"]]],
        showscale=True,
        colorbar=dict(
            title=dict(text="Stress", font=dict(color="white")),
            tickfont=dict(color="white")
        )
    ),
    name="Affordability Stress Index"
))
fig7.update_layout(
    title="Affordability Stress Index = Household Debt/GDP ÷ Savings Rate "
          "— Rising Every Year Since 2015",
    **BASE_LAYOUT, height=320
)
fig7.update_yaxes(title_text="Stress Index")
st.plotly_chart(fig7, use_container_width=True)
st.caption(
    "This index combines both sides of the affordability equation: "
    "how much debt households carry relative to the savings buffer "
    "available to absorb shocks. "
    "It has risen 43% since 2015 and shows no sign of plateauing. "
    "For context: a household with 23% debt-to-GDP and a 16.5% savings rate "
    "has far less margin for error than one with 17% debt and a 21% savings rate — "
    "even if their absolute income is higher."
)

# ─────────────────────────────────────────────────────────────
# CHAPTER 4 — DIGITAL CREDIT
# ─────────────────────────────────────────────────────────────

st.markdown(
    '<div class="chapter-header"><h3 style="margin:0">'
    'UPI Built the Road — Fintechs Drove the Truck'
    '</h3></div>',
    unsafe_allow_html=True
)

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
    layout8 = BASE_LAYOUT.copy()
    layout8["legend"] = {**BASE_LAYOUT["legend"],
                         "orientation": "h", "x": 0, "y": -0.28}
    fig8.update_layout(
        title="Credit Cards — From Niche to Normal",
        **layout8
    )
    fig8.update_yaxes(title_text="Cards (Mn)",
                      secondary_y=False, gridcolor=C["grid"], color="white")
    fig8.update_yaxes(title_text="Spends (₹ Bn)",
                      secondary_y=True,  gridcolor=C["grid"], color="white")
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
    layout9 = BASE_LAYOUT.copy()
    layout9["legend"] = {**BASE_LAYOUT["legend"],
                         "orientation": "h", "x": 0, "y": -0.28}
    fig9.update_layout(
        title="UPI Normalised Transactions — BNPL Monetised Them",
        **layout9
    )
    fig9.update_yaxes(title_text="UPI Transactions (Bn)",
                      secondary_y=False, gridcolor=C["grid"], color="white")
    fig9.update_yaxes(title_text="BNPL Users (Mn)",
                      secondary_y=True,  gridcolor=C["grid"], color="white")
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
    layout10 = BASE_LAYOUT.copy()
    layout10["legend"] = {**BASE_LAYOUT["legend"],
                          "orientation": "h", "x": 0, "y": -0.28}
    fig10.update_layout(
        title="Digital Lending Volume — 100x in 9 Years",
        **layout10
    )
    fig10.update_yaxes(title_text="₹ Billion")
    st.plotly_chart(fig10, use_container_width=True)

st.caption(
    "UPI didn't create credit — it created the behavioural habit of "
    "frictionless digital transactions that BNPL and digital lenders "
    "then monetised. ₹150 Bn in digital lending in 2015 became ₹15,000 Bn "
    "by 2024. The speed matters: it took traditional banks 30 years to "
    "build the retail credit book that fintechs doubled in 5. "
    "RBI's 2022 digital lending guidelines were a direct response to "
    "the risks this speed created."
)

# ─────────────────────────────────────────────────────────────
# CHAPTER 5 — MACRO CONTEXT
# ─────────────────────────────────────────────────────────────

st.markdown(
    '<div class="chapter-header"><h3 style="margin:0">'
    'Cheap Money Made It Easy — What Happens When It Gets Expensive?'
    '</h3></div>',
    unsafe_allow_html=True
)

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
        marker_color=C["teal"], opacity=0.35
    ), secondary_y=True)
    fig11.add_hline(y=4.0, line_dash="dot", line_color=C["grey"],
                    annotation_text="RBI 4% target",
                    annotation_font_color=C["grey"])
    layout11 = BASE_LAYOUT.copy()
    layout11["legend"] = {**BASE_LAYOUT["legend"],
                          "orientation": "h", "x": 0, "y": -0.28}
    fig11.update_layout(
        title="Repo Rate & Inflation vs Retail Credit Growth",
        **layout11
    )
    fig11.update_yaxes(title_text="Rate / Inflation %",
                       secondary_y=False, gridcolor=C["grid"], color="white")
    fig11.update_yaxes(title_text="Credit Growth %",
                       secondary_y=True,  gridcolor=C["grid"], color="white")
    st.plotly_chart(fig11, use_container_width=True)
    st.caption(
        "Repo rate sat at 4% from 2020 to 2022 — the cheapest money "
        "in modern Indian banking history. Credit growth accelerated. "
        "Then RBI hiked 250bps in 8 months. "
        "Credit growth barely slowed. "
        "That is the most important data point in this entire dashboard: "
        "when rate hikes don't cool credit demand, "
        "it means the demand is no longer discretionary."
    )

with col2:
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
            title=dict(text="r", font=dict(color="white")),
            tickfont=dict(color="white")
        )
    ))
    layout12 = BASE_LAYOUT.copy()
    layout12["xaxis"] = {**BASE_LAYOUT["xaxis"],
                         "tickfont": dict(size=9), "tickangle": 45}
    layout12["yaxis"] = {**BASE_LAYOUT["yaxis"],
                         "tickfont": dict(size=9)}
    fig12.update_layout(
        title="Correlation Matrix — What Moves With What",
        **layout12
    )
    st.plotly_chart(fig12, use_container_width=True)
    st.caption(
        "Two numbers stand out. Savings rate and household debt: -0.97. "
        "Almost perfectly inverse — as one goes up, the other goes down, "
        "with almost no exceptions across 20 years. "
        "And credit growth vs wage growth: +0.31 — weakly positive, "
        "meaning credit growth and wage growth are only loosely connected. "
        "Borrowing doesn't wait for raises."
    )

# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("## What the Data Actually Says")

s1, s2, s3, s4, s5 = st.columns(5)
kpi_card(s1, "Household Debt Rise",  "2.8x", "", None)
kpi_card(s2, "Personal Loan Growth", "31x",  "", None)
kpi_card(s3, "Savings Rate Drop",    "−7pp", "", None)
kpi_card(s4, "Digital Lending Jump", "100x", "", None)
kpi_card(s5, "Credit Cards Issued",  "5.3x", "", None)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
Between 2005 and 2024, the average Indian household went from borrowing
8.5% of GDP to 23.5% — a shift that happened quietly, EMI by EMI.

The growth wasn't uniform. Home loans, the traditional form of household
debt, grew 18x. Personal loans — the category that includes everything from
medical emergencies to vacation financing — grew **31x**.
Credit cards went from 20 million in circulation to 108 million.
Digital lenders, barely measurable in 2015, disbursed ₹15,000 billion in 2024.

The structural concern isn't the borrowing itself.
India's credit-to-GDP at 56% is still well below China (180%) or
South Korea (160%). The concern is the gap between credit growth and
wage growth — credit has outpaced wages every year since 2016 by an
average of 14 percentage points. At some point, the EMI has to be paid.

The 2020 COVID stress test gave a preview: credit card NPAs hit 6.5%,
education loan NPAs hit 8.8%. Both recovered quickly.
But the next shock may not be as short — and the savings buffer to absorb
it is 7 percentage points thinner than it was a decade ago.
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