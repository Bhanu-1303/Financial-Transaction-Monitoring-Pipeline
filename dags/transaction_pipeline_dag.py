"""
Airflow DAG for Phase 2.

This DAG will:
1. Check if a new transaction CSV exists in GCS.
2. Trigger the Dataflow job.
3. Run a BigQuery query to create a daily spending report.
"""
