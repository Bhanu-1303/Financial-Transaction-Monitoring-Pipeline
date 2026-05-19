"""
Apache Beam pipeline for Phase 2.

This pipeline will:
1. Read transaction CSV data from Google Cloud Storage.
2. Clean and validate transaction records.
3. Convert transaction amounts to USD.
4. Write cleaned records to BigQuery.
"""
