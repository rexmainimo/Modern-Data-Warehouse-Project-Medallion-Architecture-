from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.models.baseoperator import chain


default_args = {
    "owner": "Rex Mainimo",
    "retries": 1,
}

with DAG(
    dag_id="ecommerce_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # -------------------------
    # Bronze
    # -------------------------
    # Bronze ingestion is a single task that runs all the bronze scripts. 
    # Bronze logic is trivial for now.
    
    bronze_ingest = BashOperator(
        task_id="bronze_ingest",
        bash_command="python /opt/airflow/src/bronze/run_bronze.py"
    )

    # -------------------------
    # Silver
    # -------------------------
    # silver transformations are separate tasks to allow for better error logging and easier 
    # troubleshooting. Each script is called directly to ensure any errors are logged in Airflow.
    # silver transfomrations are complex unlike bronze, so I want to be able to easily identify
    # which script is failing if there are any issues.
   
    silver_customers = BashOperator(
        task_id="silver_customers",
        bash_command="python /opt/airflow/src/pipelines/run_silver_customers.py"
    )

    silver_products = BashOperator(
        task_id="silver_products",
        bash_command="python /opt/airflow/src/pipelines/run_silver_products.py"
    )

    silver_orders = BashOperator(
        task_id="silver_orders",
        bash_command="python /opt/airflow/src/pipelines/run_silver_orders.py"
    )

    silver_order_items = BashOperator(
        task_id="silver_order_items",
        bash_command="python /opt/airflow/src/pipelines/run_silver_order_items.py"
    )

    silver_web_events = BashOperator(
        task_id="silver_web_events",
        bash_command="python /opt/airflow/src/pipelines/run_silver_web_events.py"
    )

    silver_fx = BashOperator(
        task_id="silver_exchange_rates",
        bash_command="python /opt/airflow/src/pipelines/run_silver_exchange_rates.py"
    )

    # -------------------------
    # Gold Dimensions
    # -------------------------
    # gold ingestion is also separated into dimensions and facts. Dimensions are independent of 
    # each other, so they can run in parallel after silver is complete. Facts depend on all 
    # dimensions, so they will run after all dimensions are complete.
    # I call each script directly to ensure any errors are logged in Airflow and easier 
    # troubleshooting if there are any issues with the transformations in the future.
    dim_customers = BashOperator(
        task_id="dim_customers",
        bash_command="python /opt/airflow/src/pipelines/run_dim_customers.py"
    )

    dim_products = BashOperator(
        task_id="dim_products",
        bash_command="python /opt/airflow/src/pipelines/run_dim_products.py"
    )

    dim_date = BashOperator(
        task_id="dim_date",
        bash_command="python /opt/airflow/src/pipelines/run_dim_date.py"
    )

    # -------------------------
    # Gold Facts
    # -------------------------
    fact_orders = BashOperator(
        task_id="fact_orders",
        bash_command="python /opt/airflow/src/pipelines/run_fact_orders.py"
    )

    fact_order_items = BashOperator(
        task_id="fact_order_items",
        bash_command="python /opt/airflow/src/pipelines/run_fact_order_items.py"
    )

    fact_web_events = BashOperator(
        task_id="fact_web_events",
        bash_command="python /opt/airflow/src/pipelines/run_fact_web_events.py"
    )

    # -------------------------
    # PostgreSQL Load
    # -------------------------
    # Finally, I load to PostGreSQL. Might as well call it directly here to ensure any errors 
    # are logged in Airflow and easier troubleshooting if there are any issues with the load in the future.
    load_postgres = BashOperator(
        task_id="load_postgres",
        bash_command="python /opt/airflow/src/pipelines/load_to_postgres.py"
    )

    # -------------------------
    # Dependencies
    # -------------------------

    silver_tasks = [
        silver_customers,
        silver_products,
        silver_orders,
        silver_order_items,
        silver_web_events,
        silver_fx
    ]

    dim_tasks = [
        dim_customers,
        dim_products,
        dim_date
    ]

    fact_tasks = [
        fact_orders,
        fact_order_items,
        fact_web_events
    ]

    # Bronze → Silver
    bronze_ingest >> silver_tasks

    # Silver → Dimensions
    for s in silver_tasks:
        for d in dim_tasks:
            s >> d

    # Dimensions → Facts
    for d in dim_tasks:
        for f in fact_tasks:
            d >> f

    # Facts → PostgreSQL
    fact_tasks >> load_postgres

