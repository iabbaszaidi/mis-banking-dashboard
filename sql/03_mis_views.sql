-- =============================================================
-- 03_mis_views.sql
-- MIS Banking Dashboard — Reporting Views (MS SQL Server)
-- =============================================================

USE MIS_Banking;
GO

-- ── View 1: Monthly KPI Summary ───────────────────────────────
CREATE OR ALTER VIEW vw_monthly_kpi AS
SELECT
    month,
    year,
    COUNT(txn_id)                                           AS total_transactions,
    COUNT(DISTINCT customer_id)                             AS unique_customers,
    ROUND(SUM(amount_pkr), 0)                               AS total_portfolio_pkr,
    ROUND(SUM(target_pkr), 0)                               AS total_target_pkr,
    ROUND(SUM(amount_pkr) / NULLIF(SUM(target_pkr), 0) * 100, 1) AS achievement_pct,
    ROUND(SUM(CASE WHEN category = 'Assets'   THEN amount_pkr ELSE 0 END), 0) AS assets_portfolio_pkr,
    ROUND(SUM(CASE WHEN category = 'Deposits' THEN amount_pkr ELSE 0 END), 0) AS deposits_portfolio_pkr,
    ROUND(SUM(CASE WHEN category = 'Wealth'   THEN amount_pkr ELSE 0 END), 0) AS wealth_aum_pkr
FROM dbo.fact_transactions
WHERE status = 'Completed'
GROUP BY month, year;
GO

-- ── View 2: Channel Scorecard ─────────────────────────────────
CREATE OR ALTER VIEW vw_channel_scorecard AS
SELECT
    month,
    branch,
    channel,
    COUNT(txn_id)                                                   AS txn_count,
    COUNT(DISTINCT customer_id)                                     AS unique_customers,
    ROUND(SUM(amount_pkr), 0)                                       AS total_amount_pkr,
    ROUND(SUM(target_pkr), 0)                                       AS total_target_pkr,
    ROUND(SUM(amount_pkr) / NULLIF(SUM(target_pkr), 0) * 100, 1)   AS achievement_pct,
    ROUND(SUM(amount_pkr) - SUM(target_pkr), 0)                     AS variance_pkr,
    RANK() OVER (PARTITION BY month ORDER BY SUM(amount_pkr) DESC)  AS branch_rank
FROM dbo.fact_transactions
WHERE status = 'Completed'
GROUP BY month, branch, channel;
GO

-- ── View 3: Product Breakdown ──────────────────────────────────
CREATE OR ALTER VIEW vw_product_breakdown AS
SELECT
    month,
    category,
    product_name,
    COUNT(txn_id)                                                   AS txn_count,
    ROUND(SUM(amount_pkr), 0)                                       AS amount_pkr,
    ROUND(SUM(target_pkr), 0)                                       AS target_pkr,
    ROUND(SUM(amount_pkr) / NULLIF(SUM(target_pkr), 0) * 100, 1)   AS achievement_pct,
    ROUND(AVG(amount_pkr), 0)                                       AS avg_ticket_pkr
FROM dbo.fact_transactions
WHERE status = 'Completed'
GROUP BY month, category, product_name;
GO

-- ── View 4: Segment Analysis ──────────────────────────────────
CREATE OR ALTER VIEW vw_segment_analysis AS
SELECT
    month,
    segment,
    COUNT(DISTINCT customer_id)     AS unique_customers,
    COUNT(txn_id)                   AS txn_count,
    ROUND(SUM(amount_pkr), 0)       AS total_amount_pkr,
    ROUND(AVG(amount_pkr), 0)       AS avg_ticket_pkr,
    ROUND(MAX(amount_pkr), 0)       AS max_ticket_pkr
FROM dbo.fact_transactions
WHERE status = 'Completed'
GROUP BY month, segment;
GO

-- ── View 5: Executive MIS Summary ─────────────────────────────
CREATE OR ALTER VIEW vw_executive_mis AS
SELECT
    t.month,
    t.year,
    t.total_portfolio_pkr,
    t.total_target_pkr,
    t.achievement_pct,
    t.assets_portfolio_pkr,
    t.deposits_portfolio_pkr,
    t.wealth_aum_pkr,
    t.unique_customers,
    -- MoM growth using LAG
    ROUND(
        (t.total_portfolio_pkr - LAG(t.total_portfolio_pkr) OVER (ORDER BY t.month)) /
        NULLIF(LAG(t.total_portfolio_pkr) OVER (ORDER BY t.month), 0) * 100
    , 1) AS mom_growth_pct
FROM vw_monthly_kpi t;
GO

PRINT '✅ All MIS views created successfully.';
GO
