"""
Apache Beam pipeline for Phase 2.

This pipeline will:
1. Read transaction CSV data from Google Cloud Storage.
2. Clean and validate transaction records.
3. Convert transaction amounts to USD.
4. Write cleaned records to BigQuery.
"""


CURRENCY_TO_USD = {
    "USD": 1.00,
    "EUR": 1.08,
    "GBP": 1.27,
    "INR": 0.012,
    "CAD": 0.73,
}

BIGQUERY_SCHEMA = {
    "fields": [
        {"name": "transcation_id", "type": "STRING", "mode": "REQUIRED"},
        {"name": "user_id", "type": "STRING", "mode": "REQUIRED"},
        {"name": "transcation_timestamp", "type": "timestamp", "mode": "REQUIRED"},
        {"name": "orginal_amout", "type": "NUMERIC", "mode": "REQUIRED"},
        {"name": "currency", "type": "STRING", "mode": "REQUIRED"},
        {"name": "amount_usd", "type": "NUMERIC", "mode": "REQUIRED"},
        {"name": "ingestion_timestamp", "type": "NUMERIC", "mode": "REQUIRED"},
    ]
}
