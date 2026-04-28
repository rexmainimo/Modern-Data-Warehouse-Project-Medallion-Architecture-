## 📦 Modern Data Warehouse – Medallion Architecture
    ** Production-style data pipeline with orchestration, data modeling, and warehouse loading
### 📌 Overview

This project demonstrates an end-to-end data engineering pipeline implementing a Medallion Architecture (Bronze → Silver → Gold) using Python, Airflow, and PostgreSQL.

The pipeline ingests raw data, processes it into clean datasets, and loads analytical models into a data warehouse for reporting and business insights.


## 🏗️ Architecture
Raw Data → Bronze → Silver → Gold → PostgreSQL (DWH)
                ↓
             Airflow (Orchestration)
---

### ⚙️ Tech Stack
- Python (ETL pipelines)
- SQL (data modeling & transformations, Star Schema)
- Apache Airflow (orchestration)
- PostgreSQL (data warehouse)
- Parquet (data storage format)
- Docker (environment setup)
- SQLAlchemy (database connection)

---
## 🔄 Pipeline Flow
### 1. Bronze Layer
- Raw ingestion from source systems
- Stored as partitioned Parquet files
- Schema preserved

### 2. Silver Layer
- Data cleaning & transformation
- Type normalization
- Deduplication
- Handling schema drift
### 3. Gold Layer
- Star schema modeling
- Dimension tables:
-dim_customers
-dim_products
-dim_date
-Fact tables:
-fact_orders
-fact_order_items
-fact_web_events
-🗄️ Data Warehouse (PostgreSQL)
Schemas:
    bronze
    silver
    gold
    Data loaded using Python + SQLAlchemy
    Automated via Airflow DAG
    ⚡ Orchestration (Airflow)
    DAG: ecommerce_pipeline
    Tasks:
    Data ingestion
    Transformation
    Load to PostgreSQL
    Includes:
    Retry handling
    Task dependencies
    Logging

### 🚧 Challenges & Solutions
❌ SQLAlchemy transaction error
- Issue: .commit() not supported on connection
- Fix: Switched to engine.begin() for transaction handling
### ❌ PostgreSQL authentication issue
- Issue: Wrong user credentials
- Fix: Aligned credentials across Airflow & database client

## 📊 Business Value
- Enables structured analytics on:
- Revenue trends
- Customer behavior
- Product performance
- Provides clean datasets for BI tools (Power BI, Tableau)

## 🚀 Future Improvements
- Add dbt for transformation layer
- Implement data quality checks
- Add CI/CD pipeline
- Deploy to cloud (AWS/GCP/Azure)

