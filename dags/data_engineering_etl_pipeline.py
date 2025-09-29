from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


# ----------------------------
# Default Arguments
# ----------------------------
default_args = {
    'owner': 'manuelbomi',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=3)
}


# ----------------------------
# ETL Python Functions
# ----------------------------

def extract():
    print("Extracting data from source system (e.g., API, database, or CSV)")
    # Imagine loading from S3, a DB, etc.
    # return data

def transform():
    print("Transforming data: cleaning, filtering, joining, aggregating")
    # Use pandas or Spark if needed

def load():
    print("Loading transformed data into destination (e.g., warehouse or data lake)")
    # Save to Postgres, Snowflake, etc.


# ----------------------------
# DAG Definition
# ----------------------------

with DAG(
    dag_id='data_engineering_etl_pipeline_v3',
    default_args=default_args,
    description='A typical ETL pipeline for data engineering using Airflow',
    start_date=datetime(2023, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['data-engineering', 'etl', 'pipeline']
) as dag:

    task_extract = PythonOperator(
        task_id='extract_data',
        python_callable=extract
    )

    task_transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform
    )

    task_load = PythonOperator(
        task_id='load_data',
        python_callable=load
    )

    # Set task dependencies
    task_extract >> task_transform >> task_load
