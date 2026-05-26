# 📊 MIS Reporting & Sales Analytics Dashboard
### Banking Sector — Wealth & Retail Banking Performance Tracker

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![SQL Server](https://img.shields.io/badge/MS%20SQL%20Server-2019-red?logo=microsoftsqlserver)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📌 Project Overview

This project simulates a **Management Information Systems (MIS)** reporting pipeline for a banking environment, focusing on **Wealth and Retail Banking** performance tracking. It covers the full data lifecycle — from raw transaction ingestion to automated reporting and interactive Power BI dashboards.

Built to mirror real-world bank reporting workflows including:
- Monthly, quarterly, and annual **sales performance reports**
- **Assets, Deposits, and Wealth product** analytics
- **Sales channel performance scorecards**
- KPI tracking dashboards for senior management

---

## 🏗️ Project Architecture

```
mis_dashboard/
│
├── data/                        # Sample datasets (CSV)
│   ├── transactions.csv         # Raw banking transactions
│   ├── customers.csv            # Customer master data
│   └── products.csv             # Product catalog (Assets, Deposits, Wealth)
│
├── sql/                         # MS SQL Server scripts
│   ├── 01_create_tables.sql     # Schema creation
│   ├── 02_load_data.sql         # Data loading
│   ├── 03_mis_views.sql         # MIS reporting views
│   └── 04_scorecards.sql        # Sales channel scorecard queries
│
├── python/                      # Python automation scripts
│   ├── generate_data.py         # Synthetic data generator
│   ├── etl_pipeline.py          # ETL: extract, transform, load
│   ├── mis_report.py            # Automated MIS report generator
│   └── validation.py            # Data quality & validation checks
│
├── powerbi_guide/               # Power BI setup instructions
│   └── dashboard_guide.md       # Step-by-step dashboard recreation guide
│
├── docs/
│   └── project_report.md        # Full project documentation
│
└── README.md
```

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Database | MS SQL Server / PostgreSQL |
| ETL & Analysis | Python (Pandas, NumPy, SQLAlchemy) |
| Reporting | Power BI Desktop |
| Data Validation | Python (custom checks) |
| Version Control | Git / GitHub |

---

## 📊 Key Features

### 1. MIS Reporting Engine
- Automated month-end, quarterly, and annual report generation
- KPI calculations: revenue, AUM growth, deposit balances, loan disbursements
- Variance analysis vs. targets and prior periods

### 2. Sales Channel Performance Scorecards
- Branch-wise and channel-wise performance breakdown
- Product penetration rates across Assets, Deposits, Wealth
- Ranking and trend analysis per sales team

### 3. Data Quality & Validation
- Automated checks for missing values, duplicates, and anomalies
- Reconciliation between source data and reports
- Audit trail logging for data changes

### 4. Power BI Dashboard
- Interactive slicers: by month, quarter, product, branch, channel
- KPI cards, trend lines, waterfall charts
- Executive summary view + drill-down detail pages

---

## 🚀 How to Run

### Step 1 — Generate Sample Data
```bash
pip install -r requirements.txt
python python/generate_data.py
```

### Step 2 — Set Up Database
Run SQL scripts in order in MS SQL Server Management Studio (SSMS):
```sql
-- Run in order:
01_create_tables.sql
02_load_data.sql
03_mis_views.sql
04_scorecards.sql
```

### Step 3 — Run ETL Pipeline
```bash
# Update DB connection string in etl_pipeline.py first
python python/etl_pipeline.py
```

### Step 4 — Generate MIS Report
```bash
python python/mis_report.py
# Output: reports/MIS_Report_<month>.xlsx
```

### Step 5 — Power BI Dashboard
See `powerbi_guide/dashboard_guide.md` for step-by-step instructions.

---

## 📈 Sample KPIs Tracked

| KPI | Description |
|-----|-------------|
| Total Deposits | Sum of all deposit balances by product |
| Asset Portfolio Size | Total loan & asset disbursements |
| Wealth AUM | Assets Under Management for Wealth products |
| Channel Sales Score | Weighted scorecard per branch/channel |
| MoM Growth % | Month-over-month growth rate |
| Target Achievement % | Actual vs. target performance |

---

## 👤 Author

**Mohammad Abbas**  
Data Analyst | BSc Software Engineering — University of Karachi (2025)  
📧 mohammadabbas456@outlook.com  
🔗 [LinkedIn](https://linkedin.com/in/mohammad-abbas-a23951248)

---

## 📄 License
MIT License — free to use and adapt.
