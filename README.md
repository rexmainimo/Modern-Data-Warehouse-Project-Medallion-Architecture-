# Modern-Data-Warehouse-Project-Medallion-Architecture-

📊 Modern Data Warehouse – Medallion Architecture

🚀 Overview

This project implements an end-to-end data warehouse using a Medallion Architecture (Bronze → Silver → Gold) built with Python and Parquet.

It simulates a real-world analytics engineering workflow: ingesting raw data, cleaning and standardizing it, and transforming it into a dimensional model ready for business reporting.

🏗 Architecture
🥉 Bronze Layer

Raw data ingestion (partitioned Parquet)

Minimal transformation

Schema preservation

🥈 Silver Layer

Cleaned and standardized datasets

Data type normalization

Deduplication logic

Schema enforcement

Exchange rate preparation

🥇 Gold Layer (Star Schema)

Analytics-ready dimensional model with surrogate keys.

Dimensions

dim_customers

dim_products

dim_date

Fact Tables

fact_orders (1 row per order)

fact_order_items (1 row per product per order)

fact_web_events (1 row per web event)

The model supports retail sales analytics and digital engagement analysis.

📈 Business Domains Modeled

Customers

Products

Orders

Order Items

Web Events

Exchange Rates (currency normalization)

🛠 Tech Stack

Python

Pandas

PyArrow

Parquet

Dimensional Modeling (Star Schema)

Medallion Architecture

🎯 What This Project Demonstrates

End-to-end data pipeline design

Practical implementation of Medallion Architecture

Dimensional modeling with conformed dimensions

Fact table design at multiple grains

Revenue normalization with exchange rates

Real-world schema and data type troubleshooting

Clean, modular pipeline structure
