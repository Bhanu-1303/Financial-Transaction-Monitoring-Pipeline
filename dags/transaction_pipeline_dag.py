"""
Airflow DAG for Phase 2.

This DAG will:
1. Check if a new transaction CSV exists in GCS.
2. Trigger the Dataflow job.
3. Run a BigQuery query to create a daily spending report.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator


PROJECT_ID = "project-1efe30f5-674d-42ae-924"
REGION = "us-central1"
BUCKET_NAME = "financial-tranctions-data"

INPUT_FILE = "raw/mock_credit_card_transactions.csv"

DAG_ID = "financial_transaction_pipeline_phase2"


default_args = {
    "owner": "bhanu",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description="Phase 2 automated transaction pipeline using GCS, Dataflow, and BigQuery",
    start_date=datetime(2026, 5, 24),
    schedule_interval=None,
    catchup=False,
    tags=["gcs", "dataflow", "bigquery", "phase2"],
) as dag:

    start = EmptyOperator(
        task_id="start_pipeline"
    )

    end = EmptyOperator(
        task_id="end_pipeline"
    )

    start >> end
