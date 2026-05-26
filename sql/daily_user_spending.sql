-- Phase 2 reporting query
-- This query will aggregate daily spending per user_id.

CREATE OR REPLACE TABLE `project-1efe30f5-674d-42ae-924.financial_transactions.daily_user_spending` AS

SELECT
    DATE(transaction_timestamp) AS transaction_date,
    user_id,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_usd), 2) AS total_daily_spending_usd,
    ROUND(AVG(amount_usd), 2) AS average_transaction_amount_usd,
    CURRENT_TIMESTAMP
() AS report_created_at
FROM `project-1efe30f5-674d-42ae-924.financial_transactions.credit_card_transactions_clean_dataflow`
GROUP BY
  transaction_date,
  user_id
ORDER BY
  transaction_date,
  user_id;