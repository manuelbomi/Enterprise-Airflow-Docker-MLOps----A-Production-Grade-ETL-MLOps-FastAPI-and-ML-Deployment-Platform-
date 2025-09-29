from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'manuelbomi',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

# Note that max value of xcoms is 48KB, so do not use it to share big values
def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f"Hello world, my name is {first_name } {last_name},  and I am {age} years old.")

def get_name(ti):
    ti.xcom_push(key='first_name', value='Emmanuel')
    ti.xcom_push(key='last_name', value='Oyekanlu')

def get_age(ti):
    ti.xcom_push(key='age', value=2)  


with DAG(
    default_args=default_args,
    dag_id='dags_with_python_xcom_v5',
    description='using python operator instead of bash operator',
    start_date=datetime(2024, 1, 1),
    schedule='@daily'                        # or a cron string like '0 2 * * *'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet
        #op_kwargs={'age:2}
    )   

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )

    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )


    [task2 , task3] >> task1    #Here, task1 is downstream of task2 since we should first push the name to xcom before we pull it