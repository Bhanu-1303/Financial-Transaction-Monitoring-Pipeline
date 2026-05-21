"""
Apache Beam pipeline for Phase 2.

This pipeline will:
1. Read transaction CSV data from Google Cloud Storage.
2. Clean and validate transaction records.
3. Convert transaction amounts to USD.
4. Write cleaned records to BigQuery.
"""

import argparse
import csv
import logging
from datetime import datetime, timezone
from io import StringIO

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


def parse_csv_line(line):
    """
    Converting one CSV line into a cleaned transaction dictionary.

    Invalid rows return None.
    """

    try:
        reader = csv.DictReader(
            StringIO(line),
            fieldnames=[
                "transaction_id",
                "user_id",
                "timestamp",
                "merchant_category",
                "amount",
                "currency",
            ],

        )

        row = next(reader)

        transaction_id = row["transaction_id"].strip()
        user_id = row["user_id"].strip()
        timestamp_value = row["timestamp"].strip()
        merchant_category = row["merchant_category"].strip()
        currency = row["currency"].strip().upper()

        if not transaction_id or not user_id or not currency:
            return None

        amount = float(row["amount"])

        if amount < 0:
            return None

        if currency not in CURRENCY_TO_USD:
            return None

        amount_usd = round(amount * CURRENCY_TO_USD[currency], 2)
