"""
mis_report.py
-------------
Automated MIS Report Generator for Wealth & Retail Banking.
Reads data from CSV/DB, computes KPIs, and exports to Excel
with formatted sheets — simulating monthly bank MIS reporting.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

DATA_DIR = "../data"
OUTPUT_DIR = "../reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

REPORT_MONTH = "2025-01"  # Change to generate for any month (YYYY-MM)

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
def load_data():
    txn = pd.read_csv(f"{DATA_DIR}/transactions.csv", parse_dates=["txn_date"])
    cust = pd.read_csv(f"{DATA_DIR}/customers.csv")
    prod = pd.read_csv(f"{DATA_DIR}/products.csv")
    # Exclude reversals
    txn = txn[txn["status"] != "Reversed"]
    return txn, cust, prod

# ─── KPI COMPUTATION ─────────────────────────────────────────────────────────
def compute_kpis(txn):
    # Current month
    current = txn[txn["month"] == REPORT_MONTH].copy()
    # Previous month
    prev_month = pd.Period(REPORT_MONTH, freq="M") - 1
    prev = txn[txn["month"] == str(prev_month)].copy()

    def safe_growth(curr_val, prev_val):
        if prev_val == 0:
            return 0.0
        return round(((curr_val - prev_val) / prev_val) * 100, 1)

    total_amt = current["amount_pkr"].sum()
    prev_amt = prev["amount_pkr"].sum()
    total_target = current["target_pkr"].sum()

    kpis = {
        "Report Month": REPORT_MONTH,
        "Total Portfolio (PKR)": round(total_amt, 0),
        "Total Target (PKR)": round(total_target, 0),
        "Target Achievement (%)": round((total_amt / total_target * 100) if total_target else 0, 1),
        "MoM Growth (%)": safe_growth(total_amt, prev_amt),
        "Total Transactions": len(current),
        "Unique Customers": current["customer_id"].nunique(),
        "Assets Portfolio (PKR)": round(current[current["category"] == "Assets"]["amount_pkr"].sum(), 0),
        "Deposits Portfolio (PKR)": round(current[current["category"] == "Deposits"]["amount_pkr"].sum(), 0),
        "Wealth AUM (PKR)": round(current[current["category"] == "Wealth"]["amount_pkr"].sum(), 0),
    }
    return kpis, current

# ─── CHANNEL SCORECARD ────────────────────────────────────────────────────────
def channel_scorecard(current):
    scorecard = current.groupby(["branch", "channel"]).agg(
        Total_Amount=("amount_pkr", "sum"),
        Total_Target=("target_pkr", "sum"),
        Txn_Count=("txn_id", "count"),
        Unique_Customers=("customer_id", "nunique"),
    ).reset_index()
    scorecard["Achievement_%"] = round((scorecard["Total_Amount"] / scorecard["Total_Target"]) * 100, 1)
    scorecard["Variance_PKR"] = scorecard["Total_Amount"] - scorecard["Total_Target"]
    scorecard.sort_values("Achievement_%", ascending=False, inplace=True)
    scorecard["Rank"] = range(1, len(scorecard) + 1)
    return scorecard

# ─── PRODUCT BREAKDOWN ────────────────────────────────────────────────────────
def product_breakdown(current):
    breakdown = current.groupby(["category", "product_name"]).agg(
        Amount_PKR=("amount_pkr", "sum"),
        Target_PKR=("target_pkr", "sum"),
        Count=("txn_id", "count"),
    ).reset_index()
    breakdown["Achievement_%"] = round((breakdown["Amount_PKR"] / breakdown["Target_PKR"]) * 100, 1)
    breakdown.sort_values(["category", "Amount_PKR"], ascending=[True, False], inplace=True)
    return breakdown

# ─── SEGMENT ANALYSIS ─────────────────────────────────────────────────────────
def segment_analysis(current):
    seg = current.groupby("segment").agg(
        Customers=("customer_id", "nunique"),
        Total_Amount=("amount_pkr", "sum"),
        Avg_Ticket=("amount_pkr", "mean"),
    ).reset_index()
    seg["Portfolio_%"] = round((seg["Total_Amount"] / seg["Total_Amount"].sum()) * 100, 1)
    seg["Avg_Ticket"] = seg["Avg_Ticket"].round(0)
    seg.sort_values("Total_Amount", ascending=False, inplace=True)
    return seg

# ─── MONTHLY TREND ────────────────────────────────────────────────────────────
def monthly_trend(txn):
    trend = txn.groupby("month").agg(
        Total_Amount=("amount_pkr", "sum"),
        Total_Target=("target_pkr", "sum"),
        Txn_Count=("txn_id", "count"),
    ).reset_index()
    trend["Achievement_%"] = round((trend["Total_Amount"] / trend["Total_Target"]) * 100, 1)
    trend["MoM_Growth_%"] = trend["Total_Amount"].pct_change() * 100
    trend["MoM_Growth_%"] = trend["MoM_Growth_%"].round(1)
    return trend

# ─── EXPORT TO EXCEL ──────────────────────────────────────────────────────────
def export_report(kpis, scorecard, product_df, segment_df, trend_df):
    filename = f"{OUTPUT_DIR}/MIS_Report_{REPORT_MONTH}.xlsx"
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        # Sheet 1: KPI Summary
        kpi_df = pd.DataFrame(list(kpis.items()), columns=["KPI", "Value"])
        kpi_df.to_excel(writer, sheet_name="KPI Summary", index=False)

        # Sheet 2: Channel Scorecard
        scorecard.to_excel(writer, sheet_name="Channel Scorecard", index=False)

        # Sheet 3: Product Breakdown
        product_df.to_excel(writer, sheet_name="Product Breakdown", index=False)

        # Sheet 4: Segment Analysis
        segment_df.to_excel(writer, sheet_name="Segment Analysis", index=False)

        # Sheet 5: Monthly Trend
        trend_df.to_excel(writer, sheet_name="Monthly Trend", index=False)

    print(f"\n✅ MIS Report exported: {filename}")
    return filename

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n🏦 Generating MIS Report for {REPORT_MONTH}...\n")
    txn, cust, prod = load_data()
    kpis, current_month_txn = compute_kpis(txn)

    print("📊 Key KPIs:")
    for k, v in kpis.items():
        print(f"   {k}: {v:,.1f}" if isinstance(v, float) else f"   {k}: {v:,}" if isinstance(v, int) else f"   {k}: {v}")

    scorecard = channel_scorecard(current_month_txn)
    product_df = product_breakdown(current_month_txn)
    segment_df = segment_analysis(current_month_txn)
    trend_df = monthly_trend(txn)

    export_report(kpis, scorecard, product_df, segment_df, trend_df)
