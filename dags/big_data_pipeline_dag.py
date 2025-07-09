from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2025, 7, 8),
}

with DAG(
    dag_id='big_data_pipeline',
    default_args=default_args,
    schedule_interval=None,  # você pode colocar '0 8 * * *' para agendar todo dia 8h, por exemplo
    catchup=False,
    tags=['pipeline', 'orquestrador'],
    description='Pipeline completo: raw -> bronze -> silver -> gold',
) as dag:

    generate_data = BashOperator(
        task_id='generate_raw_data',
        bash_command='python scripts/generate_data.py',
    )

    bronze_transform = BashOperator(
        task_id='transform_to_bronze',
        bash_command='python scripts/transform_bronze.py',
    )

    silver_transform = BashOperator(
        task_id='transform_to_silver',
        bash_command='python scripts/transform_silver.py',
    )

    gold_transform = BashOperator(
        task_id='transform_to_gold',
        bash_command='python scripts/transform_gold.py',
    )

    # Definindo a sequência: raw → bronze → silver → gold
    generate_data >> bronze_transform >> silver_transform >> gold_transform
