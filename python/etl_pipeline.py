"""
etl_pipeline.py
---------------
ETL pipeline: Extracts CSV data, transforms/validates it,
and loads into MS SQL Server (or PostgreSQL) for MIS reporting.
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import logging
import os
from datetime import datetime

# ─── LOGGING ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("etl_log.txt")
    ]
)
log = logging.getLogger(__name__)

# ─── CONFIG — UPDATE THIS ─────────────────────────────────────────────────────
# For MS SQL Server:
DB_CONNECTION = "mssql+pyodbc://username:password@server/MIS_Banking?driver=ODBC+Driver+17+for+SQL+Server"

# For PostgreSQL (alternative):
# DB_CONNECTION = "postgresql://username:password@localhost/mis_banking"

DATA_DIR = "../data"

# ─── EXTRACT ──────────────────────────────────────────────────────────────────
def extract():
    log.info("📥 Extracting data from CSV files...")
    customers = pd.read_csv(f"{DATA_DIR}/customers.csv")
    products = pd.read_csv(f"{DATA_DIR}/products.csv")
    transactions = pd.read_csv(f"{DATA_DIR}/transactions.csv")
    log.info(f"   Customers: {len(customers)} | Products: {len(products)} | Transactions: {len(transactions)}")
    return customers, products, transactions

# ─── TRANSFORM ────────────────────────────────────────────────────────────────
def transform(customers, products, transactions):
    log.info("⚙️  Transforming data...")

    # --- Customers ---
    customers["join_date"] = pd.to_datetime(customers["join_date"])
    customers["customer_tenure_days"] = (datetime.now() - customers["join_date"]).dt.days
    customers.drop_duplicates(subset="customer_id", inplace=True)

    # --- Products ---
    products.drop_duplicates(subset="product_id", inplace=True)

    # --- Transactions ---
    transactions["txn_date"] = pd.to_datetime(transactions["txn_date"])
    transactions["month"] = pd.to_datetime(transactions["month"])
    transactions = transactions[transactions["status"] != "Reversed"]  # Exclude reversals

    # Derived columns
    transactions["variance_pkr"] = transactions["amount_pkr"] - transactions["target_pkr"]
    transactions["is_target_met"] = transactions["target_achievement_pct"] >= 100

    # Month/Quarter labels
    transactions["month_name"] = transactions["txn_date"].dt.strftime("%b %Y")
    transactions["year"] = transactions["txn_date"].dt.year

    log.info(f"   After transformation: {len(transactions)} valid transactions")
    return customers, products, transactions

# ─── VALIDATE ─────────────────────────────────────────────────────────────────
def validate(customers, products, transactions):
    log.info("✅ Running data validation checks...")
    errors = []

    # Check nulls
    for col in ["txn_id", "customer_id", "product_id", "amount_pkr", "txn_date"]:
        nulls = transactions[col].isnull().sum()
        if nulls > 0:
            errors.append(f"NULL values in {col}: {nulls}")

    # Check negative amounts
    neg = (transactions["amount_pkr"] <= 0).sum()
    if neg > 0:
        errors.append(f"Negative/zero amounts found: {neg} records")

    # Check referential integrity
    invalid_custs = ~transactions["customer_id"].isin(customers["customer_id"])
    if invalid_custs.sum() > 0:
        errors.append(f"Transactions with invalid customer_id: {invalid_custs.sum()}")

    invalid_prods = ~transactions["product_id"].isin(products["product_id"])
    if invalid_prods.sum() > 0:
        errors.append(f"Transactions with invalid product_id: {invalid_prods.sum()}")

    # Duplicate txn IDs
    dupes = transactions["txn_id"].duplicated().sum()
    if dupes > 0:
        errors.append(f"Duplicate txn_ids found: {dupes}")

    if errors:
        for e in errors:
            log.warning(f"   ⚠️  {e}")
    else:
        log.info("   All validation checks passed ✓")

    return len(errors) == 0

# ─── LOAD ─────────────────────────────────────────────────────────────────────
def load(customers, products, transactions):
    log.info("📤 Loading data into database...")
    try:
        engine = create_engine(DB_CONNECTION)
        with engine.connect() as conn:
            customers.to_sql("dim_customers", conn, if_exists="replace", index=False)
            log.info("   ✅ dim_customers loaded")

            products.to_sql("dim_products", conn, if_exists="replace", index=False)
            log.info("   ✅ dim_products loaded")

            transactions.to_sql("fact_transactions", conn, if_exists="replace", index=False)
            log.info("   ✅ fact_transactions loaded")

        log.info("🏁 ETL pipeline complete.")
    except Exception as e:
        log.error(f"❌ Database load failed: {e}")
        log.info("💡 Check your DB_CONNECTION string in etl_pipeline.py")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    log.info("\n🏦 Starting MIS Banking ETL Pipeline\n")
    customers, products, transactions = extract()
    customers, products, transactions = transform(customers, products, transactions)
    is_valid = validate(customers, products, transactions)
    if is_valid:
        load(customers, products, transactions)
    else:
        log.error("❌ Validation failed. Fix data issues before loading.")
