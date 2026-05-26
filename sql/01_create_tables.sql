-- =============================================================
-- 01_create_tables.sql
-- MIS Banking Dashboard — Schema Creation (MS SQL Server)
-- =============================================================

USE MIS_Banking;
GO

-- Drop if exists
IF OBJECT_ID('dbo.fact_transactions', 'U') IS NOT NULL DROP TABLE dbo.fact_transactions;
IF OBJECT_ID('dbo.dim_customers', 'U') IS NOT NULL DROP TABLE dbo.dim_customers;
IF OBJECT_ID('dbo.dim_products', 'U') IS NOT NULL DROP TABLE dbo.dim_products;
GO

-- ── Dimension: Customers ──────────────────────────────────────
CREATE TABLE dbo.dim_customers (
    customer_id         VARCHAR(10)     PRIMARY KEY,
    name                VARCHAR(100)    NOT NULL,
    segment             VARCHAR(30)     NOT NULL,
    branch              VARCHAR(50)     NOT NULL,
    channel             VARCHAR(50)     NOT NULL,
    join_date           DATE            NOT NULL,
    city                VARCHAR(50)     NOT NULL,
    customer_tenure_days INT            NULL,
    CONSTRAINT chk_segment CHECK (segment IN ('Mass Market', 'Emerging Affluent', 'Affluent', 'Private Banking'))
);
GO

-- ── Dimension: Products ───────────────────────────────────────
CREATE TABLE dbo.dim_products (
    product_id          VARCHAR(10)     PRIMARY KEY,
    product_name        VARCHAR(100)    NOT NULL,
    category            VARCHAR(20)     NOT NULL,
    min_amount          DECIMAL(18,2)   NOT NULL,
    max_amount          DECIMAL(18,2)   NOT NULL,
    target_monthly      INT             NOT NULL,
    CONSTRAINT chk_category CHECK (category IN ('Assets', 'Deposits', 'Wealth'))
);
GO

-- ── Fact: Transactions ────────────────────────────────────────
CREATE TABLE dbo.fact_transactions (
    txn_id                  VARCHAR(12)     PRIMARY KEY,
    customer_id             VARCHAR(10)     NOT NULL REFERENCES dbo.dim_customers(customer_id),
    product_id              VARCHAR(10)     NOT NULL REFERENCES dbo.dim_products(product_id),
    product_name            VARCHAR(100)    NOT NULL,
    category                VARCHAR(20)     NOT NULL,
    branch                  VARCHAR(50)     NOT NULL,
    channel                 VARCHAR(50)     NOT NULL,
    segment                 VARCHAR(30)     NOT NULL,
    txn_date                DATE            NOT NULL,
    month                   VARCHAR(7)      NOT NULL,   -- YYYY-MM
    quarter                 VARCHAR(10)     NOT NULL,   -- Q1 2025
    amount_pkr              DECIMAL(18,2)   NOT NULL,
    target_pkr              DECIMAL(18,2)   NOT NULL,
    target_achievement_pct  DECIMAL(6,1)    NOT NULL,
    variance_pkr            DECIMAL(18,2)   NULL,
    is_target_met           BIT             NULL,
    month_name              VARCHAR(20)     NULL,
    year                    INT             NULL,
    status                  VARCHAR(20)     NOT NULL,
    CONSTRAINT chk_status CHECK (status IN ('Completed', 'Pending', 'Reversed')),
    CONSTRAINT chk_amount CHECK (amount_pkr > 0)
);
GO

PRINT '✅ All tables created successfully.';
GO
