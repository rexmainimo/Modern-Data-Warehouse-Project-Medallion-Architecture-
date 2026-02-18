# Modern-Data-Warehouse-Project-Medallion-Architecture-

📊 Modern Data Warehouse (Medallion Architecture)
🚀 Overview

This project implements an end-to-end data warehouse using a Medallion Architecture (Bronze → Silver → Gold) with Python and Parquet.

It simulates a real-world data engineering pipeline including raw ingestion, schema standardization, data transformation, and dimensional modeling.

🏗 Architecture

Bronze

Raw data ingestion

Partitioned Parquet files

Minimal transformation

Silver

Cleaned and standardized datasets

Schema enforcement

Data type normalization

Deduplication

Gold

Star schema modeling

Dimension tables with surrogate keys

Analytics-ready datasets

✅ Implemented
Data Domains

Customers

Products

Orders

Web Events

Exchange Rates

Gold Dimensions

dim_customers

dim_products

dim_date

Engineering Highlights

Partitioned Parquet handling

Schema drift resolution

Bronze schema maintenance layer

Currency normalization foundation

Clean directory structure & modular scripts

🔜 Next Step

Implement fact_orders

Implement fact_web_events

Join exchange rates for normalized revenue analytics

🛠 Tech Stack

Python

Pandas

PyArrow

Parquet

Star Schema modeling

🎯 What This Demonstrates

End-to-end data pipeline design

Medallion architecture implementation

Data warehouse modeling fundamentals

Real-world schema troubleshooting
