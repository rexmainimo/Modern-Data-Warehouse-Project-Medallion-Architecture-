from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="ecommerce_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    bronze = BashOperator(
        task_id="bronze",
        bash_command="python /opt/airflow/src/bronze/run_bronze.py"
    )

    silver = BashOperator(
        task_id="silver",
        bash_command="python /opt/airflow/src/silver/run_silver.py"
    )

    gold = BashOperator(
        task_id="gold",
        bash_command="python /opt/airflow/src/gold/run_gold.py"
    )

    load = BashOperator(
        task_id="load",
        bash_command="python /opt/airflow/src/load/run_load.py"
    )

    bronze >> silver >> gold >> load