import os

print("Running Silver transformations...")

os.system("python /opt/airflow/src/silver/transform_customers.py")
os.system("python /opt/airflow/src/silver/transform_orders.py")
os.system("python /opt/airflow/src/silver/transform_products.py")
os.system("python /opt/airflow/src/silver/transform_web_events.py")
os.system("python /opt/airflow/src/silver/transform_exchange_rates.py")

print("Silver layer completed")