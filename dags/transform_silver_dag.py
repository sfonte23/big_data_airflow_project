from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2025, 7, 8),
}

with DAG(
    dag_id='transform_silver',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['pipeline'],
    description='Limpa e trata dados da camada bronze para silver',
) as dag:

    transform = BashOperator(
        task_id='clean_and_filter_data',
        bash_command='python scripts/transform_silver.py',
    )
