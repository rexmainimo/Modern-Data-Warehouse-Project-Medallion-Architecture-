import os

print("Loading into PostgreSQL...")

os.system("python /opt/airflow/src/load/load_dim_customers.py")
os.system("python /opt/airflow/src/load/load_dim_products.py")
os.system("python /opt/airflow/src/load/load_dim_date.py")

os.system("python /opt/airflow/src/load/load_fact_orders.py")
os.system("python /opt/airflow/src/load/load_fact_order_items.py")
os.system("python /opt/airflow/src/load/load_fact_web_events.py")

print("Data loaded to PostgreSQL")