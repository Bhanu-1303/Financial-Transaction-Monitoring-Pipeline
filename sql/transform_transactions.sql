CREATE OR REPLACE TABLE `project-1efe30f5-674d-42ae-924.financial_transactions.credict_card_transactions_clean` AS

WITH
    cleaned
    AS
    (
        SELECT
            NULLIF(TRIM(transaction_id), '') AS transaction_id,
            NULLIF(TRIM(user_id), '') AS user_id,
            SAFE_CAST(timestamp AS TIMESTAMP) AS transaction_timestamp,
            NULLIF(TRIM(merchant_category), '') AS merchant_category,
            SAFE_CAST(amount AS NUMERIC) AS amount,
            NULLIF(TRIM(currency), '') AS currency,
            CURRENT_TIMESTAMP AS ingestion_timestamp
        FROM `project-1efe30f5-674d-42ae-924.financial_transactions.ext_credict_card_transactions`

),

deduplicated AS
(
    SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY transaction_id
      ORDER BY transaction_timestamp DESC
    ) AS row_num
FROM cleaned
WHERE transaction_id IS NOT NULL
    AND user_id IS NOT NULL
    AND transaction_timestamp IS NOT NULL
    AND merchant_category IS NOT NULL
    AND amount is NOT NULL
    AND amount >= 0
    AND currency IS NOT NULL
)

SELECT
    transaction_id,
    user_id,
    transaction_timestamp,
    merchant_category,
    amount,
    currency,
    ingestion_timestamp
FROM deduplicated
where row_num = 1;

