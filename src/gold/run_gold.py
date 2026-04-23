import os

print("Building Gold layer...")

os.system("python /opt/airflow/src/gold/build_dim_customers.py")
os.system("python /opt/airflow/src/gold/build_dim_products.py")
os.system("python /opt/airflow/src/gold/build_dim_date.py")

os.system("python /opt/airflow/src/gold/build_fact_orders.py")
os.system("python /opt/airflow/src/gold/build_fact_order_items.py")
os.system("python /opt/airflow/src/gold/build_fact_web_events.py")

print("Gold layer completed")