import os
# I use this for local testing of the silver transformations. 
# ecommerce_pipeline calls them directly to ensure error logging if any script fails and easier troubleshooting.

print("Running Silver transformations...")

os.system("python /opt/airflow/src/silver/transform_customers.py")
os.system("python /opt/airflow/src/silver/transform_orders.py")
os.system("python /opt/airflow/src/silver/transform_orderItems.py")
os.system("python /opt/airflow/src/silver/transform_products.py")
os.system("python /opt/airflow/src/silver/transform_web_events.py")
os.system("python /opt/airflow/src/silver/transform_exchange_rates.py")

print("Silver layer completed")
#from src.silver.transform_customers import main