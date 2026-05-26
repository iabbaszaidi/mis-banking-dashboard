"""
generate_data.py
----------------
Generates synthetic banking transaction data for the MIS Dashboard project.
Simulates Wealth & Retail Banking data: Assets, Deposits, Wealth products.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

random.seed(42)
np.random.seed(42)

OUTPUT_DIR = "../data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── CONFIG ──────────────────────────────────────────────────────────────────
N_CUSTOMERS = 500
N_TRANSACTIONS = 5000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 3, 31)

BRANCHES = ["Clifton", "DHA", "Gulshan", "PECHS", "Saddar", "Johar", "Malir", "North Nazimabad"]
CHANNELS = ["Branch", "Digital", "Relationship Manager", "Call Center"]
PRODUCTS = {
    "Assets":   ["Home Loan", "Auto Loan", "Personal Loan", "Business Finance"],
    "Deposits": ["Current Account", "Savings Account", "Term Deposit", "Foreign Currency Deposit"],
    "Wealth":   ["Mutual Fund", "Investment Advisory", "Insurance", "Pension Fund"],
}
SEGMENTS = ["Mass Market", "Emerging Affluent", "Affluent", "Private Banking"]

# ─── GENERATE CUSTOMERS ───────────────────────────────────────────────────────
def generate_customers():
    customers = []
    for i in range(1, N_CUSTOMERS + 1):
        segment = np.random.choice(SEGMENTS, p=[0.50, 0.25, 0.18, 0.07])
        customers.append({
            "customer_id": f"CUST{i:04d}",
            "name": f"Customer_{i}",
            "segment": segment,
            "branch": random.choice(BRANCHES),
            "channel": random.choice(CHANNELS),
            "join_date": START_DATE - timedelta(days=random.randint(30, 1000)),
            "city": "Karachi",
        })
    df = pd.DataFrame(customers)
    df.to_csv(f"{OUTPUT_DIR}/customers.csv", index=False)
    print(f"✅ customers.csv — {len(df)} records")
    return df

# ─── GENERATE PRODUCTS ────────────────────────────────────────────────────────
def generate_products():
    products = []
    pid = 1
    for category, items in PRODUCTS.items():
        for item in items:
            products.append({
                "product_id": f"PROD{pid:03d}",
                "product_name": item,
                "category": category,
                "min_amount": 10000 if category == "Assets" else 5000,
                "max_amount": 5000000 if category == "Assets" else 2000000,
                "target_monthly": random.randint(50, 200),
            })
            pid += 1
    df = pd.DataFrame(products)
    df.to_csv(f"{OUTPUT_DIR}/products.csv", index=False)
    print(f"✅ products.csv — {len(df)} records")
    return df

# ─── GENERATE TRANSACTIONS ────────────────────────────────────────────────────
def generate_transactions(customers_df, products_df):
    transactions = []
    date_range = (END_DATE - START_DATE).days

    for i in range(1, N_TRANSACTIONS + 1):
        customer = customers_df.sample(1).iloc[0]
        product = products_df.sample(1).iloc[0]
        txn_date = START_DATE + timedelta(days=random.randint(0, date_range))

        # Amount based on segment
        multiplier = {"Mass Market": 1, "Emerging Affluent": 2.5, "Affluent": 6, "Private Banking": 20}
        base_amount = random.uniform(product["min_amount"], product["max_amount"])
        amount = round(base_amount * multiplier[customer["segment"]], 2)

        # Target achievement (simulated)
        target = round(amount * random.uniform(0.7, 1.3), 2)
        achieved_pct = round((amount / target) * 100, 1)

        transactions.append({
            "txn_id": f"TXN{i:06d}",
            "customer_id": customer["customer_id"],
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],
            "branch": customer["branch"],
            "channel": customer["channel"],
            "segment": customer["segment"],
            "txn_date": txn_date.strftime("%Y-%m-%d"),
            "month": txn_date.strftime("%Y-%m"),
            "quarter": f"Q{(txn_date.month - 1) // 3 + 1} {txn_date.year}",
            "amount_pkr": amount,
            "target_pkr": target,
            "target_achievement_pct": achieved_pct,
            "status": random.choice(["Completed", "Completed", "Completed", "Pending", "Reversed"]),
        })

    df = pd.DataFrame(transactions)
    df.to_csv(f"{OUTPUT_DIR}/transactions.csv", index=False)
    print(f"✅ transactions.csv — {len(df)} records")
    return df

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🏦 Generating MIS Banking Dataset...\n")
    customers = generate_customers()
    products = generate_products()
    transactions = generate_transactions(customers, products)
    print("\n✅ All data files generated in /data folder.")
    print("   Run etl_pipeline.py next to load into SQL Server.")
