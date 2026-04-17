# Modern Data Warehouse Project (Medallion Architecture)

## 📊 Overview
This project implements an end-to-end data warehouse using a Medallion Architecture (Bronze → Silver → Gold) built with Python and Parquet, and extended with PostgreSQL for analytical querying.

It simulates a real-world analytics engineering workflow: ingesting raw data, cleaning and standardizing it, and transforming it into a dimensional model ready for business reporting.

---

## 🏗 Architecture

### 🥉 Bronze Layer
- Raw data ingestion (CSV, JSON, API)
- Stored as partitioned Parquet files
- Minimal transformation, schema preserved

### 🥈 Silver Layer
- Cleaned and standardized datasets
- Data type normalization and schema enforcement
- Deduplication logic applied
- Exchange rates prepared for currency normalization

### 🥇 Gold Layer (Star Schema)
Analytics-ready dimensional model with surrogate keys.

**Dimensions**
- dim_customers  
- dim_products  
- dim_date  

**Fact Tables**
- fact_orders (1 row per order)  
- fact_order_items (1 row per product per order)  
- fact_web_events (1 row per web event)  

Supports both **sales analytics** and **user behavior analysis**.

---

## 🗄 Data Warehouse Layer
- Gold layer loaded into **PostgreSQL**
- Enables SQL-based querying and validation
- Tested using DBeaver

---

## 📈 Business Domains Modeled
- Customers  
- Products  
- Orders  
- Order Items  
- Web Events  
- Exchange Rates (currency normalization)

---

## 🛠 Tech Stack
- Python  
- Pandas  
- PyArrow  
- Parquet  
- PostgreSQL  
- Dimensional Modeling (Star Schema)  
- Medallion Architecture  

---

## 🎯 What This Project Demonstrates
- End-to-end data pipeline design  
- Medallion architecture implementation  
- Dimensional modeling with multiple fact table grains  
- Currency normalization using exchange rates  
- Handling real-world data issues (schema drift, nulls, type conflicts)  
- Building a queryable data warehouse (PostgreSQL)  
- Clean, modular pipeline structure  

---

## 🔜 Next Steps
- Workflow orchestration with Airflow  
- Containerization using Docker Compose  
- Incremental loading strategies (replace → append/upsert)  