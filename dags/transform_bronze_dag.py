from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2025, 7, 8),
}

with DAG(
    dag_id='transform_bronze',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['pipeline'],
    description='Transforma JSON em banco SQLite na camada Bronze',
) as dag:

    transform = BashOperator(
        task_id='transform_json_to_bronze',
        bash_command='python scripts/transform_bronze.py',
    )
