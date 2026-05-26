"""
validation.py
-------------
Standalone data quality and validation checks for MIS reporting.
Ensures accuracy, consistency, and reliability of banking data
before it enters the reporting pipeline.
"""

import pandas as pd
import numpy as np
from datetime import datetime

DATA_DIR = "../data"

def run_all_checks():
    print("\n🔍 Running MIS Data Validation Suite\n" + "="*45)

    txn = pd.read_csv(f"{DATA_DIR}/transactions.csv", parse_dates=["txn_date"])
    cust = pd.read_csv(f"{DATA_DIR}/customers.csv")
    prod = pd.read_csv(f"{DATA_DIR}/products.csv")

    results = []

    def check(name, condition, count=None):
        status = "✅ PASS" if condition else "❌ FAIL"
        results.append({"Check": name, "Status": status, "Detail": count})
        print(f"  {status}  {name}" + (f" ({count})" if count else ""))

    # ── Completeness Checks ──────────────────────────────────────
    print("\n📋 Completeness Checks:")
    for col in ["txn_id", "customer_id", "product_id", "amount_pkr", "txn_date", "status"]:
        nulls = txn[col].isnull().sum()
        check(f"No NULLs in {col}", nulls == 0, f"{nulls} nulls found" if nulls else None)

    # ── Uniqueness Checks ────────────────────────────────────────
    print("\n🔑 Uniqueness Checks:")
    dup_txn = txn["txn_id"].duplicated().sum()
    check("Unique txn_id", dup_txn == 0, f"{dup_txn} duplicates" if dup_txn else None)

    dup_cust = cust["customer_id"].duplicated().sum()
    check("Unique customer_id", dup_cust == 0, f"{dup_cust} duplicates" if dup_cust else None)

    # ── Referential Integrity ────────────────────────────────────
    print("\n🔗 Referential Integrity:")
    invalid_cust = (~txn["customer_id"].isin(cust["customer_id"])).sum()
    check("All txn customer_ids exist in customers", invalid_cust == 0, f"{invalid_cust} orphan records")

    invalid_prod = (~txn["product_id"].isin(prod["product_id"])).sum()
    check("All txn product_ids exist in products", invalid_prod == 0, f"{invalid_prod} orphan records")

    # ── Validity Checks ──────────────────────────────────────────
    print("\n✔️  Validity Checks:")
    neg_amounts = (txn["amount_pkr"] <= 0).sum()
    check("No negative/zero amounts", neg_amounts == 0, f"{neg_amounts} records")

    valid_statuses = {"Completed", "Pending", "Reversed"}
    invalid_status = (~txn["status"].isin(valid_statuses)).sum()
    check("Valid status values only", invalid_status == 0, f"{invalid_status} invalid statuses")

    future_txns = (txn["txn_date"] > datetime.now()).sum()
    check("No future-dated transactions", future_txns == 0, f"{future_txns} future records")

    valid_categories = {"Assets", "Deposits", "Wealth"}
    invalid_cats = (~txn["category"].isin(valid_categories)).sum()
    check("Valid product categories", invalid_cats == 0, f"{invalid_cats} invalid categories")

    # ── Consistency Checks ───────────────────────────────────────
    print("\n🔄 Consistency Checks:")
    pct_mismatch = txn.copy()
    pct_mismatch["computed_pct"] = (pct_mismatch["amount_pkr"] / pct_mismatch["target_pkr"] * 100).round(1)
    mismatch = (abs(pct_mismatch["computed_pct"] - pct_mismatch["target_achievement_pct"]) > 1).sum()
    check("Achievement % consistent with amounts", mismatch == 0, f"{mismatch} mismatches")

    # ── Summary ──────────────────────────────────────────────────
    results_df = pd.DataFrame(results)
    passed = results_df["Status"].str.contains("PASS").sum()
    failed = results_df["Status"].str.contains("FAIL").sum()

    print(f"\n{'='*45}")
    print(f"📊 Validation Summary: {passed} passed | {failed} failed")
    if failed == 0:
        print("🏁 Data is clean and ready for MIS reporting ✅")
    else:
        print("⚠️  Fix failing checks before loading into reporting pipeline.")
    print("="*45 + "\n")

    return results_df

if __name__ == "__main__":
    run_all_checks()
