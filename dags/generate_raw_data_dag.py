from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2025, 7, 8),
}

with DAG(
    dag_id='generate_raw_data',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['pipeline'],
    description='Gera dados falsos e salva em JSON (camada raw)',
) as dag:

    generate_data = BashOperator(
        task_id='generate_fake_users',
        bash_command='python scripts/generate_data.py',
    )
