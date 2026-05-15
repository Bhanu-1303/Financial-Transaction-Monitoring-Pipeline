CREATE OR REPLACE EXTERNAL TABLE `project-1efe30f5-674d-42ae-924.financial_transactions.ext_credict_card_transactions`
(
    transaction_id  STRING,
    user_id  STRING,
    timestamp STRING,
    merchant_category STRING,
    amount STRING,
    currency STRING
)
OPTIONS
(
    format = 'CSV',
    uris = ['gs://financial-tranctions-data/raw/mock_credit_card_transactions.csv'],
    skip_leading_rows = 1
);