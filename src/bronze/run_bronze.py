import os

print("Running Bronze ingestion...")

os.system("python /opt/airflow/src/bronze/bronze_ingest_customers.py")
os.system("python /opt/airflow/src/bronze/bronze_ingest_orders.py")
os.system("python /opt/airflow/src/bronze/bronze_ingest_products.py")
os.system("python /opt/airflow/src/bronze/bronze_ingest_web_events.py")
os.system("python /opt/airflow/src/bronze/bronze_ingest_exchange_rates.py")

print("Bronze layer completed")