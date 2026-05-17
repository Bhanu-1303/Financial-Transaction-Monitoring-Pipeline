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
```

## Tools and Technologies Used

Python, Faker, Google Cloud Storage, BigQuery, SQL, Git, GitHub, VS Code

## Dataset Description

The mock dataset contains 100,000 fake credit card transaction records.

Columns included:

Column	Description
transaction_id	Unique ID for each transaction
user_id	Fake user/customer ID
timestamp	Date and time of the transaction
merchant_category	Category of the merchant
amount	Transaction amount
currency	Currency used for the transaction
