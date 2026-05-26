-- =============================================================
-- 04_scorecards.sql
-- MIS Banking Dashboard — Sales Performance Scorecards
-- =============================================================

USE MIS_Banking;
GO

-- ── Scorecard 1: Monthly Branch Performance ───────────────────
-- Top performing branches by achievement % for a given month
SELECT TOP 10
    branch,
    channel,
    SUM(amount_pkr)                                                 AS total_sales_pkr,
    SUM(target_pkr)                                                 AS total_target_pkr,
    ROUND(SUM(amount_pkr)/NULLIF(SUM(target_pkr),0)*100, 1)        AS achievement_pct,
    ROUND(SUM(amount_pkr) - SUM(target_pkr), 0)                    AS variance_pkr,
    COUNT(DISTINCT customer_id)                                     AS customers_served,
    RANK() OVER (ORDER BY SUM(amount_pkr)/NULLIF(SUM(target_pkr),0) DESC) AS rank
FROM dbo.fact_transactions
WHERE month = '2025-01'          -- Change month as needed
  AND status = 'Completed'
GROUP BY branch, channel
ORDER BY achievement_pct DESC;
GO

-- ── Scorecard 2: Product Category Contribution ────────────────
SELECT
    category,
    product_name,
    COUNT(txn_id)                                                   AS transactions,
    ROUND(SUM(amount_pkr),0)                                        AS amount_pkr,
    ROUND(SUM(amount_pkr)*100.0 / SUM(SUM(amount_pkr)) OVER (), 1) AS portfolio_share_pct,
    ROUND(AVG(amount_pkr),0)                                        AS avg_ticket_pkr
FROM dbo.fact_transactions
WHERE month = '2025-01'
  AND status = 'Completed'
GROUP BY category, product_name
ORDER BY category, amount_pkr DESC;
GO

-- ── Scorecard 3: QTD (Quarter-to-Date) Summary ────────────────
SELECT
    quarter,
    category,
    ROUND(SUM(amount_pkr),0)                                         AS qtd_amount_pkr,
    ROUND(SUM(target_pkr),0)                                         AS qtd_target_pkr,
    ROUND(SUM(amount_pkr)/NULLIF(SUM(target_pkr),0)*100, 1)          AS qtd_achievement_pct
FROM dbo.fact_transactions
WHERE quarter = 'Q1 2025'
  AND status = 'Completed'
GROUP BY quarter, category
ORDER BY category;
GO

-- ── Scorecard 4: Annual Performance Summary ───────────────────
SELECT
    year,
    category,
    ROUND(SUM(amount_pkr),0)                                        AS annual_amount_pkr,
    ROUND(SUM(target_pkr),0)                                        AS annual_target_pkr,
    ROUND(SUM(amount_pkr)/NULLIF(SUM(target_pkr),0)*100, 1)        AS achievement_pct,
    COUNT(DISTINCT customer_id)                                     AS unique_customers
FROM dbo.fact_transactions
WHERE year = 2024
  AND status = 'Completed'
GROUP BY year, category
ORDER BY category;
GO

-- ── Scorecard 5: Segment-Wise Portfolio Split ─────────────────
SELECT
    segment,
    COUNT(DISTINCT customer_id)                                     AS customers,
    ROUND(SUM(amount_pkr),0)                                        AS total_pkr,
    ROUND(SUM(amount_pkr)*100.0 / SUM(SUM(amount_pkr)) OVER (), 1) AS portfolio_share_pct,
    ROUND(AVG(amount_pkr),0)                                        AS avg_ticket_pkr
FROM dbo.fact_transactions
WHERE month = '2025-01'
  AND status = 'Completed'
GROUP BY segment
ORDER BY total_pkr DESC;
GO

PRINT '✅ Scorecard queries ready.';
GO
