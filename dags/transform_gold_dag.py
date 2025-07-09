from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2025, 7, 8),
}

with DAG(
    dag_id='transform_gold',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['pipeline'],
    description='Agrega os dados para a camada gold',
) as dag:

    transform = BashOperator(
        task_id='aggregate_and_save',
        bash_command='python scripts/transform_gold.py',
    )
