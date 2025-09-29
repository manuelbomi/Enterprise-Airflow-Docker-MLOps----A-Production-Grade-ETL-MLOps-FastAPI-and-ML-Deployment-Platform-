from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'manuelbomi',
    'retries': 7,
    'retry_delay': timedelta(minutes=7)
}

with DAG(
    dag_id='dag_with_catchup_backfill_v4',
    default_args=default_args,
    start_date=datetime(2023, 10, 15),
    schedule="@daily",
    catchup=False
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo "Simple bash command!"'
    )