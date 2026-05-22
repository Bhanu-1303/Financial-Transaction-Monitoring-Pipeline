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

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


CURRENCY_TO_USD = {
    "USD": 1.00,
    "EUR": 1.08,
    "GBP": 1.27,
    "INR": 0.012,
    "CAD": 0.73,
}


BIGQUERY_SCHEMA = {
    "fields": [
        {"name": "transaction_id", "type": "STRING", "mode": "REQUIRED"},
        {"name": "user_id", "type": "STRING", "mode": "REQUIRED"},
        {"name": "transaction_timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
        {"name": "merchant_category", "type": "STRING", "mode": "NULLABLE"},
        {"name": "original_amount", "type": "NUMERIC", "mode": "REQUIRED"},
        {"name": "currency", "type": "STRING", "mode": "REQUIRED"},
        {"name": "amount_usd", "type": "NUMERIC", "mode": "REQUIRED"},
        {"name": "ingestion_timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
    ]
}


def parse_csv_line(line):
    """
    Convert one CSV line into a cleaned transaction dictionary.

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

        if not transaction_id or not user_id or not timestamp_value or not currency:
            return None

        amount = float(row["amount"])

        if amount < 0:
            return None

        if currency not in CURRENCY_TO_USD:
            return None

        amount_usd = round(amount * CURRENCY_TO_USD[currency], 2)

        transaction_timestamp = datetime.strptime(
            timestamp_value.split(".")[0],
            "%Y-%m-%d %H:%M:%S",
        ).replace(tzinfo=timezone.utc)

        return {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "transaction_timestamp": transaction_timestamp.isoformat(),
            "merchant_category": merchant_category,
            "original_amount": round(amount, 2),
            "currency": currency,
            "amount_usd": amount_usd,
            "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as error:
        logging.warning(f"Invalid row skipped: {line}. Error: {error}")
        return None


def run():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="GCS input CSV path. Example: gs://bucket/raw/file.csv",
    )

    parser.add_argument(
        "--output_table",
        required=True,
        help="BigQuery output table. Example: project:dataset.table",
    )

    known_args, pipeline_args = parser.parse_known_args()

    pipeline_options = PipelineOptions(pipeline_args)

    with beam.Pipeline(options=pipeline_options) as pipeline:
        (
            pipeline
            | "Read CSV From GCS" >> beam.io.ReadFromText(
                known_args.input,
                skip_header_lines=1,
            )
            | "Parse And Clean Rows" >> beam.Map(parse_csv_line)
            | "Remove Invalid Rows" >> beam.Filter(lambda row: row is not None)
            | "Write To BigQuery" >> beam.io.WriteToBigQuery(
                known_args.output_table,
                schema=BIGQUERY_SCHEMA,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
