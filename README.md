# India's Credit Decade (2005–2024)
### How Indian Households Went From Savers to Borrowers

---

## The Question

India's household savings rate fell from 23.5% in 2005 to 16.5% in 2024.
Over the same period, household debt as a share of GDP nearly tripled.
This project asks: what drove this shift, what are Indians borrowing for,
and is it sustainable?

---

## Key Findings

- **Household debt tripled** from 8.5% of GDP (2005) to 23.5% (2024)
- **Personal loan outstanding grew 31x** since 2005 vs 18x for home loans —
  India is borrowing to consume, not just to own assets
- **Credit consistently outgrew wages since 2016** — the affordability gap
  averaged 14 percentage points per year between 2018 and 2024
- **Digital lending grew 100x** from ₹150 Bn (2015) to ₹15,000 Bn (2024),
  driven by UPI infrastructure, BNPL, and digital-first lenders
- **Savings rate and household debt correlation: −0.97** — the most direct
  quantitative evidence of India's savings-to-borrowing behavioural shift
- **Credit card NPA peaked at 6.5% during COVID** — unsecured lending is
  most vulnerable to income shocks, a key risk for retail bank portfolios

---

## Why This Matters for Banks

Indian banks are the primary beneficiaries and risk-bearers of this shift.
Retail credit now accounts for ~30% of total bank credit (up from ~15% in 2005).
The credit-wage gap signals potential stress in unsecured portfolios.
Understanding this structural shift is essential context for:
- Credit risk modelling
- Retail lending strategy
- NPA provisioning decisions
- New-to-credit segment targeting

---

## Data Sources

| Dataset | Source |
|---------|--------|
| Credit-to-GDP ratio | World Bank Open Data API |
| GDP & CPI inflation | World Bank Open Data API |
| Repo rate history | RBI Monetary Policy Statements |
| Retail credit growth by segment | RBI Handbook of Statistics (Table 29) |
| Retail NPA by segment | RBI Financial Stability Reports |
| Household debt & savings | RBI Annual Report + MOSPI |
| Credit card & UPI data | RBI Payment System Reports |
| Digital lending volumes | RBI Working Paper + industry estimates |

---

## Methodology Notes

- All credit growth figures are year-on-year percentage change
- Outstanding credit indexed to 2005 = 100 for comparability
- Affordability Stress Index = Household Debt/GDP ÷ Savings Rate
- Credit-Wage Gap = Retail Credit Growth % − Average Wage Growth %
- Digital lending data combines RBI regulated entity data with
  industry estimates for unregulated BNPL (clearly flagged in dashboard)

---

## Limitations

1. Wage growth data is aggregate — does not capture informal sector (60%+ of workforce)
2. Digital lending pre-2018 is estimated — RBI only started systematic collection in 2021
3. Annual data smooths intra-year volatility (e.g. COVID quarters)
4. Household debt figures exclude informal moneylender debt

---

## Tools

| Tool | Purpose |
|------|---------|
| Python (requests, pandas) | Data collection and processing |
| Streamlit | Interactive dashboard |
| Plotly | Visualisations |
| Power BI | Business intelligence version |

---

## How to Run

```bash
git clone https://github.com/parvatiiyer/rbi-credit.git
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python notebooks/01_data_collection.py
streamlit run notebooks/02_dashboard.py
```

---

## Live Dashboard

[Streamlit Dashboard →](https://rbi-credit-cecw9jqvbubngb6hwjk4nh.streamlit.app/)