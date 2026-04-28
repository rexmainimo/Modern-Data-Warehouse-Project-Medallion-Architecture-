from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.models.baseoperator import chain


default_args = {
    "owner": "data_engineer",
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
    bronze_ingest = BashOperator(
        task_id="bronze_ingest",
        bash_command="python /opt/airflow/src/bronze/run_bronze.py"
    )

    # -------------------------
    # Silver
    # -------------------------
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



# with DAG(
#     dag_id="ecommerce_pipeline",
#     start_date=datetime(2024, 1, 1),
#     schedule_interval=None,
#     catchup=False
# ) as dag:

#     bronze = BashOperator(
#         task_id="bronze",
#         bash_command="python /opt/airflow/src/bronze/run_bronze.py"
#     )

#     silver = BashOperator(
#         task_id="silver",
#         bash_command="python /opt/airflow/src/silver/run_silver.py"
#     )

#     gold = BashOperator(
#         task_id="gold",
#         bash_command="python /opt/airflow/src/gold/run_gold.py"
#     )

#     load = BashOperator(
#         task_id="load",
#         bash_command="python /opt/airflow/src/load/run_load.py"
#     )

#     bronze >> silver >> gold >> load