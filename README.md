# Financial Transaction Monitoring Pipeline

This project builds a beginner-to-intermediate data engineering pipeline for financial transaction data using Python, Google Cloud Storage, BigQuery, Apache Beam, Cloud Dataflow, and Cloud Composer.

The project is divided into two phases.

---

## Project Objective

The goal of this project is to simulate a real-world financial transaction data pipeline.

The pipeline generates mock credit card transaction data, uploads it to Google Cloud Storage, processes and cleans the data, writes clean records into BigQuery, and creates a daily user spending report.

---

## Phase 1: Batch ELT Foundation

In Phase 1, the pipeline follows a simple batch ELT flow:

```text
Local Python Script
        ↓
Google Cloud Storage
        ↓
BigQuery External Table
        ↓
SQL Transformation
        ↓
Clean Native BigQuery Table
```

### Phase 1 Work Completed

* Created a GitHub repository
* Created a VS Code project
* Created a Python virtual environment
* Generated 100,000 mock credit card transactions using Faker
* Saved the data as a CSV file
* Uploaded the CSV file to Google Cloud Storage
* Created a BigQuery external table pointing to the GCS file
* Cleaned and transformed the data using BigQuery SQL
* Created a clean native BigQuery table
* Pushed project files to GitHub

---

## Phase 2: Automated Cloud ETL

In Phase 2, the transformation logic was moved from SQL into Apache Beam and executed using Google Cloud Dataflow.

The workflow was also automated using Cloud Composer, which is Google Cloud's managed Apache Airflow service.

```text
Google Cloud Storage
        ↓
Cloud Dataflow / Apache Beam
        ↓
Clean BigQuery Table
        ↓
Cloud Composer / Airflow
        ↓
Daily Spending Reporting Table
```

### Phase 2 Work Completed

* Created an Apache Beam pipeline in Python
* Read transaction CSV data from Google Cloud Storage
* Parsed and cleaned transaction records
* Filtered invalid records
* Converted transaction amounts into USD using a static currency mapping
* Wrote clean transaction data directly into BigQuery
* Created a Cloud Composer environment
* Created an Airflow DAG to automate the pipeline
* Added a GCS file check task
* Added a Dataflow trigger task
* Added a BigQuery reporting query task
* Successfully tested the full Airflow DAG
* Verified Dataflow job completion
* Verified BigQuery reporting table creation

---

## Architecture

```text
Raw CSV File in GCS
        ↓
Airflow DAG starts
        ↓
Task 1: Check if file exists in GCS
        ↓
Task 2: Trigger Apache Beam pipeline on Dataflow
        ↓
Task 3: Run BigQuery daily spending aggregation
        ↓
Final reporting table created in BigQuery
```

---

## Technologies Used

* Python
* Faker
* Apache Beam
* Google Cloud Storage
* Google Cloud Dataflow
* Google BigQuery
* Google Cloud Composer
* Apache Airflow
* SQL
* Git
* GitHub
* VS Code

---

## Project Folder Structure

```text
Financial-Transaction-Monitoring-Pipeline/
│
├── Scripts/
│   ├── generate_mock_transactions.py
│   └── upload_to_gcs.py
│
├── data/
│   └── mock_credit_card_transactions.csv
│
├── dataflow/
│   └── beam_transaction_pipeline.py
│
├── dags/
│   └── transaction_pipeline_dag.py
│
├── sql/
│   ├── create_external_table.sql
│   ├── transform_transactions.sql
│   └── daily_user_spending.sql
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Dataset Columns

The mock transaction dataset contains the following columns:

| Column            | Description                   |
| ----------------- | ----------------------------- |
| transaction_id    | Unique transaction identifier |
| user_id           | Unique user identifier        |
| timestamp         | Transaction timestamp         |
| merchant_category | Category of merchant          |
| amount            | Transaction amount            |
| currency          | Transaction currency          |

---

## BigQuery Tables

### External Table

```text
financial_transactions.ext_credit_card_transactions
```

This table points directly to the raw CSV file stored in Google Cloud Storage.

### Clean Table from Phase 1

```text
financial_transactions.credit_card_transactions_clean
```

This table stores cleaned transaction data created using BigQuery SQL.

### Clean Table from Phase 2

```text
financial_transactions.credit_card_transactions_clean_dataflow
```

This table stores cleaned transaction data created by Apache Beam running on Cloud Dataflow.

### Reporting Table

```text
financial_transactions.daily_user_spending
```

This table stores daily user spending summaries.

---

## Airflow DAG Tasks

The Cloud Composer DAG includes the following tasks:

```text
start_pipeline
        ↓
check_gcs_file
        ↓
trigger_dataflow_job
        ↓
run_daily_spending_query
        ↓
end_pipeline
```

### Task Details

| Task                     | Purpose                                                |
| ------------------------ | ------------------------------------------------------ |
| start_pipeline           | Starts the DAG workflow                                |
| check_gcs_file           | Checks whether the transaction CSV exists in GCS       |
| trigger_dataflow_job     | Runs the Apache Beam pipeline on Dataflow              |
| run_daily_spending_query | Runs BigQuery SQL to create daily user spending report |
| end_pipeline             | Ends the DAG workflow                                  |

---

## Final Output

The final reporting table shows daily spending per user.

Example output columns:

| Column                         | Description                                    |
| ------------------------------ | ---------------------------------------------- |
| transaction_date               | Date of transaction                            |
| user_id                        | User identifier                                |
| transaction_count              | Number of transactions by the user on that day |
| total_daily_spending_usd       | Total daily spending in USD                    |
| average_transaction_amount_usd | Average transaction amount in USD              |
| report_created_at              | Timestamp when the report was created          |

---

## Key Learning Outcomes

Through this project, I learned how to:

* Build a batch ELT pipeline
* Generate mock data using Python
* Upload files to Google Cloud Storage
* Create BigQuery external and native tables
* Write SQL transformations in BigQuery
* Build an Apache Beam pipeline
* Run Beam pipelines using Google Cloud Dataflow
* Automate a data workflow using Cloud Composer and Airflow
* Debug IAM permission issues in GCP
* Understand how service accounts are used in cloud pipelines
* Organize and document a data engineering project on GitHub

---

## Professional Data Engineering Concepts Practiced

* Batch data processing
* Cloud storage ingestion
* Distributed data processing
* Data cleaning and validation
* Currency standardization
* BigQuery reporting tables
* Workflow orchestration
* Service account permissions
* Pipeline monitoring
* GitHub project documentation

---

## Project Status

```text
Phase 1: Completed
Phase 2: Completed
```

---

## Notes

This project was built as a learning project to understand how real-world cloud data pipelines are designed and automated using Google Cloud Platform.
