# Financial-Transaction-Monitoring-Pipeline

This project builds a beginner-friendly batch ELT pipeline for financial transaction data using Python, Google Cloud Storage, and BigQuery.

The goal of this project is to generate mock credit card transaction data, upload it to Google Cloud Storage, create a BigQuery external table, clean and transform the data using SQL, and save the final cleaned data into a native BigQuery table.

---

## Project Objective

The main objective of this project is to understand how a basic cloud data engineering pipeline works.

Pipeline flow:

```text
Local Python Script
        ↓
Mock Credit Card Transaction CSV
        ↓
Google Cloud Storage
        ↓
BigQuery External Table
        ↓
SQL Transformation
        ↓
Clean Native BigQuery Table
