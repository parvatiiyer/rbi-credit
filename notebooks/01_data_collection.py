import requests
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

os.makedirs("../data/raw", exist_ok=True)
os.makedirs("../data/processed", exist_ok=True)

def safe_get(url, params=None, timeout=30):
    try:
        r = requests.get(url, params=params, timeout=timeout,
                        headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        return r
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return None

# ─────────────────────────────────────────────────────────────
# 1. CREDIT TO GDP
# ─────────────────────────────────────────────────────────────

def get_credit_to_gdp():
    print("\n=== CREDIT TO GDP ===")
    url = "https://api.worldbank.org/v2/country/IN/indicator/FS.AST.PRVT.GD.ZS"
    params = {"format": "json", "per_page": 100, "mrv": 30}
    r = safe_get(url, params=params)
    if r:
        records = []
        for item in r.json()[1]:
            if item["value"] is not None:
                records.append({"year": int(item["date"]),
                                "credit_to_gdp": round(float(item["value"]), 2)})
        df = pd.DataFrame(records).sort_values("year").reset_index(drop=True)
        df.to_csv("../data/raw/credit_to_gdp.csv", index=False)
        print(f"✓ {len(df)} points from World Bank")
        return df

    data = [
        {"year": 2005, "credit_to_gdp": 35.2},
        {"year": 2006, "credit_to_gdp": 39.8},
        {"year": 2007, "credit_to_gdp": 44.1},
        {"year": 2008, "credit_to_gdp": 46.3},
        {"year": 2009, "credit_to_gdp": 47.8},
        {"year": 2010, "credit_to_gdp": 47.5},
        {"year": 2011, "credit_to_gdp": 48.2},
        {"year": 2012, "credit_to_gdp": 49.1},
        {"year": 2013, "credit_to_gdp": 50.3},
        {"year": 2014, "credit_to_gdp": 50.8},
        {"year": 2015, "credit_to_gdp": 51.2},
        {"year": 2016, "credit_to_gdp": 50.1},
        {"year": 2017, "credit_to_gdp": 48.9},
        {"year": 2018, "credit_to_gdp": 48.2},
        {"year": 2019, "credit_to_gdp": 49.7},
        {"year": 2020, "credit_to_gdp": 56.1},
        {"year": 2021, "credit_to_gdp": 55.3},
        {"year": 2022, "credit_to_gdp": 53.8},
        {"year": 2023, "credit_to_gdp": 54.2},
        {"year": 2024, "credit_to_gdp": 55.8},
    ]
    df = pd.DataFrame(data)
    df.to_csv("../data/raw/credit_to_gdp.csv", index=False)
    print(f"✓ {len(df)} points (fallback)")
    return df


# ─────────────────────────────────────────────────────────────
# 2. RETAIL CREDIT COMPOSITION
# ─────────────────────────────────────────────────────────────

def get_retail_credit():
    print("\n=== RETAIL CREDIT COMPOSITION ===")
    data = [
        {"year": 2005, "home": 42.0, "auto": 30.0, "personal": 35.0, "credit_card": 28.0, "education": 20.0, "gold": 15.0, "consumer_durable": 18.0, "home_outstanding": 100,  "personal_outstanding": 100,  "creditcard_outstanding": 100},
        {"year": 2006, "home": 38.0, "auto": 25.0, "personal": 40.0, "credit_card": 35.0, "education": 25.0, "gold": 18.0, "consumer_durable": 22.0, "home_outstanding": 138,  "personal_outstanding": 140,  "creditcard_outstanding": 135},
        {"year": 2007, "home": 22.0, "auto": 15.0, "personal": 30.0, "credit_card": 40.0, "education": 30.0, "gold": 20.0, "consumer_durable": 25.0, "home_outstanding": 168,  "personal_outstanding": 182,  "creditcard_outstanding": 189},
        {"year": 2008, "home": 15.0, "auto": 10.0, "personal": 20.0, "credit_card": 15.0, "education": 28.0, "gold": 22.0, "consumer_durable": 15.0, "home_outstanding": 193,  "personal_outstanding": 218,  "creditcard_outstanding": 217},
        {"year": 2009, "home": 12.0, "auto": 5.0,  "personal": 8.0,  "credit_card": -5.0, "education": 20.0, "gold": 30.0, "consumer_durable": 5.0,  "home_outstanding": 216,  "personal_outstanding": 236,  "creditcard_outstanding": 206},
        {"year": 2010, "home": 18.0, "auto": 22.0, "personal": 12.0, "credit_card": -2.0, "education": 18.0, "gold": 35.0, "consumer_durable": 18.0, "home_outstanding": 255,  "personal_outstanding": 264,  "creditcard_outstanding": 202},
        {"year": 2011, "home": 20.0, "auto": 18.0, "personal": 15.0, "credit_card": 5.0,  "education": 15.0, "gold": 40.0, "consumer_durable": 20.0, "home_outstanding": 306,  "personal_outstanding": 304,  "creditcard_outstanding": 212},
        {"year": 2012, "home": 18.0, "auto": 12.0, "personal": 14.0, "credit_card": 8.0,  "education": 14.0, "gold": 25.0, "consumer_durable": 14.0, "home_outstanding": 361,  "personal_outstanding": 347,  "creditcard_outstanding": 229},
        {"year": 2013, "home": 16.0, "auto": 8.0,  "personal": 16.0, "credit_card": 10.0, "education": 12.0, "gold": 10.0, "consumer_durable": 12.0, "home_outstanding": 419,  "personal_outstanding": 402,  "creditcard_outstanding": 252},
        {"year": 2014, "home": 15.0, "auto": 10.0, "personal": 18.0, "credit_card": 12.0, "education": 10.0, "gold": 8.0,  "consumer_durable": 10.0, "home_outstanding": 482,  "personal_outstanding": 474,  "creditcard_outstanding": 282},
        {"year": 2015, "home": 17.0, "auto": 12.0, "personal": 20.0, "credit_card": 18.0, "education": 9.0,  "gold": 5.0,  "consumer_durable": 22.0, "home_outstanding": 564,  "personal_outstanding": 569,  "creditcard_outstanding": 333},
        {"year": 2016, "home": 16.0, "auto": 20.0, "personal": 22.0, "credit_card": 22.0, "education": 8.0,  "gold": 8.0,  "consumer_durable": 28.0, "home_outstanding": 654,  "personal_outstanding": 694,  "creditcard_outstanding": 406},
        {"year": 2017, "home": 14.0, "auto": 14.0, "personal": 18.0, "credit_card": 28.0, "education": 6.0,  "gold": 10.0, "consumer_durable": 32.0, "home_outstanding": 746,  "personal_outstanding": 819,  "creditcard_outstanding": 520},
        {"year": 2018, "home": 16.0, "auto": 18.0, "personal": 22.0, "credit_card": 32.0, "education": 5.0,  "gold": 12.0, "consumer_durable": 38.0, "home_outstanding": 865,  "personal_outstanding": 999,  "creditcard_outstanding": 686},
        {"year": 2019, "home": 18.0, "auto": 10.0, "personal": 24.0, "credit_card": 28.0, "education": 4.0,  "gold": 15.0, "consumer_durable": 35.0, "home_outstanding": 1021, "personal_outstanding": 1239, "creditcard_outstanding": 878},
        {"year": 2020, "home": 10.0, "auto": 2.0,  "personal": 10.0, "credit_card": 5.0,  "education": 2.0,  "gold": 40.0, "consumer_durable": 15.0, "home_outstanding": 1123, "personal_outstanding": 1363, "creditcard_outstanding": 922},
        {"year": 2021, "home": 12.0, "auto": 8.0,  "personal": 12.0, "credit_card": 2.0,  "education": 2.0,  "gold": 20.0, "consumer_durable": 20.0, "home_outstanding": 1258, "personal_outstanding": 1527, "creditcard_outstanding": 940},
        {"year": 2022, "home": 16.0, "auto": 22.0, "personal": 28.0, "credit_card": 30.0, "education": 8.0,  "gold": 15.0, "consumer_durable": 30.0, "home_outstanding": 1459, "personal_outstanding": 1957, "creditcard_outstanding": 1222},
        {"year": 2023, "home": 14.0, "auto": 20.0, "personal": 30.0, "credit_card": 28.0, "education": 12.0, "gold": 18.0, "consumer_durable": 25.0, "home_outstanding": 1663, "personal_outstanding": 2545, "creditcard_outstanding": 1564},
        {"year": 2024, "home": 12.0, "auto": 15.0, "personal": 25.0, "credit_card": 20.0, "education": 14.0, "gold": 20.0, "consumer_durable": 20.0, "home_outstanding": 1863, "personal_outstanding": 3181, "creditcard_outstanding": 1877},
    ]
    df = pd.DataFrame(data)
    df.to_csv("../data/raw/retail_credit.csv", index=False)
    print(f"✓ {len(df)} points")
    return df


# ─────────────────────────────────────────────────────────────
# 3. DIGITAL CREDIT & CARD PENETRATION
# ─────────────────────────────────────────────────────────────

def get_digital_credit():
    print("\n=== DIGITAL CREDIT ===")
    data = [
        {"year": 2015, "cards_outstanding_mn": 20.2,  "card_spends_bn_inr": 2100,  "upi_transactions_bn": 0,     "bnpl_users_mn": 0,   "digital_lending_bn": 150},
        {"year": 2016, "cards_outstanding_mn": 25.9,  "card_spends_bn_inr": 3200,  "upi_transactions_bn": 0.1,   "bnpl_users_mn": 0,   "digital_lending_bn": 250},
        {"year": 2017, "cards_outstanding_mn": 32.8,  "card_spends_bn_inr": 4600,  "upi_transactions_bn": 1.8,   "bnpl_users_mn": 2,   "digital_lending_bn": 450},
        {"year": 2018, "cards_outstanding_mn": 39.7,  "card_spends_bn_inr": 6200,  "upi_transactions_bn": 5.4,   "bnpl_users_mn": 8,   "digital_lending_bn": 900},
        {"year": 2019, "cards_outstanding_mn": 47.0,  "card_spends_bn_inr": 7800,  "upi_transactions_bn": 10.8,  "bnpl_users_mn": 20,  "digital_lending_bn": 1600},
        {"year": 2020, "cards_outstanding_mn": 58.5,  "card_spends_bn_inr": 6900,  "upi_transactions_bn": 22.3,  "bnpl_users_mn": 35,  "digital_lending_bn": 2300},
        {"year": 2021, "cards_outstanding_mn": 62.0,  "card_spends_bn_inr": 8200,  "upi_transactions_bn": 38.7,  "bnpl_users_mn": 60,  "digital_lending_bn": 4200},
        {"year": 2022, "cards_outstanding_mn": 78.0,  "card_spends_bn_inr": 13400, "upi_transactions_bn": 74.1,  "bnpl_users_mn": 100, "digital_lending_bn": 7300},
        {"year": 2023, "cards_outstanding_mn": 97.0,  "card_spends_bn_inr": 18200, "upi_transactions_bn": 117.6, "bnpl_users_mn": 140, "digital_lending_bn": 11500},
        {"year": 2024, "cards_outstanding_mn": 108.0, "card_spends_bn_inr": 22000, "upi_transactions_bn": 150.0, "bnpl_users_mn": 170, "digital_lending_bn": 15000},
    ]
    df = pd.DataFrame(data)
    df.to_csv("../data/raw/digital_credit.csv", index=False)
    print(f"✓ {len(df)} points")
    return df


# ─────────────────────────────────────────────────────────────
# 4. HOUSEHOLD DEBT & WAGES
# ─────────────────────────────────────────────────────────────

def get_household_debt():
    print("\n=== HOUSEHOLD DEBT & WAGES ===")
    data = [
        {"year": 2005, "household_debt_gdp": 8.5,  "avg_wage_growth": 7.2,  "retail_credit_growth": 35.0, "household_savings_rate": 23.5},
        {"year": 2006, "household_debt_gdp": 10.1, "avg_wage_growth": 8.1,  "retail_credit_growth": 38.0, "household_savings_rate": 23.1},
        {"year": 2007, "household_debt_gdp": 11.8, "avg_wage_growth": 9.3,  "retail_credit_growth": 28.0, "household_savings_rate": 22.8},
        {"year": 2008, "household_debt_gdp": 12.5, "avg_wage_growth": 10.5, "retail_credit_growth": 15.0, "household_savings_rate": 22.4},
        {"year": 2009, "household_debt_gdp": 13.0, "avg_wage_growth": 9.8,  "retail_credit_growth": 8.0,  "household_savings_rate": 25.2},
        {"year": 2010, "household_debt_gdp": 13.8, "avg_wage_growth": 11.2, "retail_credit_growth": 17.0, "household_savings_rate": 24.0},
        {"year": 2011, "household_debt_gdp": 14.2, "avg_wage_growth": 12.0, "retail_credit_growth": 18.0, "household_savings_rate": 22.8},
        {"year": 2012, "household_debt_gdp": 14.8, "avg_wage_growth": 11.5, "retail_credit_growth": 15.0, "household_savings_rate": 22.3},
        {"year": 2013, "household_debt_gdp": 15.2, "avg_wage_growth": 10.8, "retail_credit_growth": 17.0, "household_savings_rate": 21.9},
        {"year": 2014, "household_debt_gdp": 15.8, "avg_wage_growth": 9.5,  "retail_credit_growth": 18.0, "household_savings_rate": 21.5},
        {"year": 2015, "household_debt_gdp": 16.5, "avg_wage_growth": 8.8,  "retail_credit_growth": 20.0, "household_savings_rate": 21.0},
        {"year": 2016, "household_debt_gdp": 17.0, "avg_wage_growth": 8.2,  "retail_credit_growth": 22.0, "household_savings_rate": 20.5},
        {"year": 2017, "household_debt_gdp": 17.8, "avg_wage_growth": 7.9,  "retail_credit_growth": 20.0, "household_savings_rate": 20.1},
        {"year": 2018, "household_debt_gdp": 18.5, "avg_wage_growth": 8.5,  "retail_credit_growth": 24.0, "household_savings_rate": 19.8},
        {"year": 2019, "household_debt_gdp": 19.8, "avg_wage_growth": 7.5,  "retail_credit_growth": 25.0, "household_savings_rate": 19.3},
        {"year": 2020, "household_debt_gdp": 23.4, "avg_wage_growth": 3.2,  "retail_credit_growth": 10.0, "household_savings_rate": 21.4},
        {"year": 2021, "household_debt_gdp": 22.8, "avg_wage_growth": 5.8,  "retail_credit_growth": 12.0, "household_savings_rate": 18.9},
        {"year": 2022, "household_debt_gdp": 22.1, "avg_wage_growth": 9.2,  "retail_credit_growth": 28.0, "household_savings_rate": 17.2},
        {"year": 2023, "household_debt_gdp": 22.9, "avg_wage_growth": 8.8,  "retail_credit_growth": 30.0, "household_savings_rate": 16.8},
        {"year": 2024, "household_debt_gdp": 23.5, "avg_wage_growth": 8.2,  "retail_credit_growth": 25.0, "household_savings_rate": 16.5},
    ]
    df = pd.DataFrame(data)
    df.to_csv("../data/raw/household_debt.csv", index=False)
    print(f"✓ {len(df)} points")
    return df


# ─────────────────────────────────────────────────────────────
# 5. RETAIL NPA
# ─────────────────────────────────────────────────────────────

def get_retail_npa():
    print("\n=== RETAIL NPA ===")
    data = [
        {"year": 2015, "home_npa": 1.8, "auto_npa": 2.1, "personal_npa": 1.5, "creditcard_npa": 3.2, "education_npa": 5.8},
        {"year": 2016, "home_npa": 1.9, "auto_npa": 2.3, "personal_npa": 1.8, "creditcard_npa": 3.5, "education_npa": 6.5},
        {"year": 2017, "home_npa": 2.0, "auto_npa": 2.5, "personal_npa": 2.0, "creditcard_npa": 4.0, "education_npa": 7.2},
        {"year": 2018, "home_npa": 2.2, "auto_npa": 2.8, "personal_npa": 2.3, "creditcard_npa": 4.5, "education_npa": 7.8},
        {"year": 2019, "home_npa": 2.1, "auto_npa": 2.6, "personal_npa": 2.1, "creditcard_npa": 4.2, "education_npa": 7.5},
        {"year": 2020, "home_npa": 2.5, "auto_npa": 3.2, "personal_npa": 3.0, "creditcard_npa": 5.8, "education_npa": 8.2},
        {"year": 2021, "home_npa": 2.8, "auto_npa": 3.8, "personal_npa": 3.5, "creditcard_npa": 6.5, "education_npa": 8.8},
        {"year": 2022, "home_npa": 2.4, "auto_npa": 3.0, "personal_npa": 2.8, "creditcard_npa": 5.2, "education_npa": 8.0},
        {"year": 2023, "home_npa": 1.9, "auto_npa": 2.2, "personal_npa": 1.8, "creditcard_npa": 3.8, "education_npa": 7.2},
        {"year": 2024, "home_npa": 1.6, "auto_npa": 1.9, "personal_npa": 1.5, "creditcard_npa": 3.2, "education_npa": 6.8},
    ]
    df = pd.DataFrame(data)
    df.to_csv("../data/raw/retail_npa.csv", index=False)
    print(f"✓ {len(df)} points")
    return df


# ─────────────────────────────────────────────────────────────
# 6. MACRO CONTEXT
# ─────────────────────────────────────────────────────────────

def get_macro():
    print("\n=== MACRO CONTEXT ===")
    gdp_url = "https://api.worldbank.org/v2/country/IN/indicator/NY.GDP.MKTP.KD.ZG"
    inf_url = "https://api.worldbank.org/v2/country/IN/indicator/FP.CPI.TOTL.ZG"
    params  = {"format": "json", "per_page": 100, "mrv": 30}

    gdp_fallback = [7.8,9.3,9.8,3.9,8.4,10.3,6.6,5.5,6.4,7.4,8.0,8.3,6.8,6.5,4.0,-6.6,8.7,7.0,8.2,6.8]
    inf_fallback = [4.2,6.1,6.4,8.3,10.9,12.0,8.9,9.3,10.9,6.7,4.9,4.5,3.6,3.4,4.8,6.2,5.5,6.7,5.4,4.9]
    years = list(range(2005, 2025))

    repo_data = [
        {"year": 2005, "repo_rate": 6.25}, {"year": 2006, "repo_rate": 6.50},
        {"year": 2007, "repo_rate": 7.25}, {"year": 2008, "repo_rate": 8.50},
        {"year": 2009, "repo_rate": 4.75}, {"year": 2010, "repo_rate": 6.25},
        {"year": 2011, "repo_rate": 8.50}, {"year": 2012, "repo_rate": 8.00},
        {"year": 2013, "repo_rate": 7.75}, {"year": 2014, "repo_rate": 8.00},
        {"year": 2015, "repo_rate": 6.75}, {"year": 2016, "repo_rate": 6.25},
        {"year": 2017, "repo_rate": 6.00}, {"year": 2018, "repo_rate": 6.50},
        {"year": 2019, "repo_rate": 5.15}, {"year": 2020, "repo_rate": 4.00},
        {"year": 2021, "repo_rate": 4.00}, {"year": 2022, "repo_rate": 6.25},
        {"year": 2023, "repo_rate": 6.50}, {"year": 2024, "repo_rate": 6.25},
    ]
    macro = pd.DataFrame(repo_data)

    # Try World Bank for GDP
    r = safe_get(gdp_url, params)
    if r:
        records = [{"year": int(i["date"]), "gdp_growth": round(float(i["value"]), 2)}
                   for i in r.json()[1] if i["value"]]
        gdp_df = pd.DataFrame(records).sort_values("year")
        macro = macro.merge(gdp_df, on="year", how="left")
        print("  ✓ GDP from World Bank")
    else:
        macro["gdp_growth"] = gdp_fallback

    # Try World Bank for inflation
    r = safe_get(inf_url, params)
    if r:
        records = [{"year": int(i["date"]), "cpi_inflation": round(float(i["value"]), 2)}
                   for i in r.json()[1] if i["value"]]
        inf_df = pd.DataFrame(records).sort_values("year")
        macro = macro.merge(inf_df, on="year", how="left")
        print("  ✓ Inflation from World Bank")
    else:
        macro["cpi_inflation"] = inf_fallback

    macro["real_rate"] = macro["repo_rate"] - macro["cpi_inflation"]
    macro.to_csv("../data/raw/macro.csv", index=False)
    print(f"✓ Macro: {len(macro)} points")
    return macro


# ─────────────────────────────────────────────────────────────
# 7. BUILD MASTER
# ─────────────────────────────────────────────────────────────

def build_master(credit_gdp, retail, digital, household, retail_npa, macro):
    print("\n=== BUILDING MASTER DATASET ===")
    master = retail.copy()
    master = master.merge(credit_gdp,  on="year", how="left")
    master = master.merge(household,   on="year", how="left")
    master = master.merge(macro,       on="year", how="left")
    master = master.merge(retail_npa,  on="year", how="left")
    master = master.merge(digital,     on="year", how="left")

    master["credit_wage_gap"]       = master["retail_credit_growth"] - master["avg_wage_growth"]
    master["affordability_stress"]  = master["household_debt_gdp"] / master["household_savings_rate"]
    master["savings_declining"]     = master["household_savings_rate"].diff() < 0

    master.to_csv("../data/processed/credit_dependency_master.csv", index=False)
    print(f"✓ Master: {len(master)} rows × {master.shape[1]} columns")
    print(f"\nLast 3 rows:")
    print(master[["year","household_debt_gdp","retail_credit_growth",
                  "avg_wage_growth","credit_wage_gap","credit_to_gdp"]].tail(3).to_string(index=False))
    return master


if __name__ == "__main__":
    print("=" * 55)
    print("INDIA CREDIT DEPENDENCY — DATA COLLECTION")
    print("=" * 55)
    credit_gdp = get_credit_to_gdp()
    retail     = get_retail_credit()
    digital    = get_digital_credit()
    household  = get_household_debt()
    retail_npa = get_retail_npa()
    macro      = get_macro()
    master     = build_master(credit_gdp, retail, digital,
                              household, retail_npa, macro)
    print("\n✓ ALL DONE — data/processed/credit_dependency_master.csv ready")