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
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.apache.beam.operators.beam import BeamRunPythonPipelineOperator


PROJECT_ID = "project-1efe30f5-674d-42ae-924"
REGION = "us-central1"
BUCKET_NAME = "financial-tranctions-data"

INPUT_FILE = "raw/mock_credit_card_transactions.csv"

DAG_ID = "financial_transaction_pipeline_phase2"

BEAM_PIPELINE_FILE = f"gs://{BUCKET_NAME}/dataflow/beam_transaction_pipeline.py"

GCS_INPUT_PATH = f"gs://{BUCKET_NAME}/{INPUT_FILE}"

BQ_OUTPUT_TABLE = (
    f"{PROJECT_ID}:financial_transactions.credit_card_transactions_clean_dataflow"
)

TEMP_LOCATION = f"gs://{BUCKET_NAME}/temp/"
STAGING_LOCATION = f"gs://{BUCKET_NAME}/staging/"


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

    "Task 1 — Check if New File Exists in GCS"

    check_gcs_file = GCSObjectExistenceSensor(
        task_id="check_gcs_file",
        bucket=BUCKET_NAME,
        object=INPUT_FILE,
        timeout=300,
        poke_interval=30,
        mode="poke",
    )

    "Task 2 - Trigger Dataflow Job from Airflow DAG"

    trigger_dataflow_job = BeamRunPythonPipelineOperator(
        task_id="trigger_dataflow_job",
        py_file=BEAM_PIPELINE_FILE,
        runner="DataflowRunner",
        pipeline_options={
            "project": PROJECT_ID,
            "region": REGION,
            "input": GCS_INPUT_PATH,
            "output_table": BQ_OUTPUT_TABLE,
            "temp_location": TEMP_LOCATION,
            "staging_location": STAGING_LOCATION,
            "job_name": "transaction-dataflow-job-airflow",
        },
        py_requirements=["apache-beam[gcp]"],
        py_system_site_packages=False,
    )

    end = EmptyOperator(
        task_id="end_pipeline"
    )

    start >> check_gcs_file >> trigger_dataflow_job >> end
