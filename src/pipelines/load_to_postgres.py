import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://airflow:airflow@postgres:5432/dwh")

# Create schemas
with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze"))
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver"))
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold"))

# Load Dimensions
pd.read_parquet("/opt/airflow/data/gold/dimensions/dim_customers.parquet") \
    .to_sql("dim_customers", engine, schema="gold", if_exists="replace", index=False)

pd.read_parquet("/opt/airflow/data/gold/dimensions/dim_products.parquet") \
    .to_sql("dim_products", engine, schema="gold", if_exists="replace", index=False)

pd.read_parquet("/opt/airflow/data/gold/dimensions/dim_date.parquet") \
    .to_sql("dim_date", engine, schema="gold", if_exists="replace", index=False)

# Load Facts
pd.read_parquet("/opt/airflow/data/gold/facts/fact_orders.parquet") \
    .to_sql("fact_orders", engine, schema="gold", if_exists="replace", index=False)

pd.read_parquet("/opt/airflow/data/gold/facts/fact_order_items.parquet") \
    .to_sql("fact_order_items", engine, schema="gold", if_exists="replace", index=False)

pd.read_parquet("/opt/airflow/data/gold/facts/fact_web_events.parquet") \
    .to_sql("fact_web_events", engine, schema="gold", if_exists="replace", index=False)

print("Data loaded into PostgreSQL successfully")