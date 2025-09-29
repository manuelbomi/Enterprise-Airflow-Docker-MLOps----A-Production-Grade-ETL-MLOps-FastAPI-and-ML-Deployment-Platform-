from datetime import datetime, timedelta
from airflow.decorators import dag, task

# ----------------------------
# Default Arguments
# ----------------------------
default_args = {
    'owner': 'manuelbomi',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

# ----------------------------
# Taskflow Functions
# ----------------------------

@dag(dag_id='dag_with_taskflow_api_v3S',
     default_args=default_args,
     start_date=datetime(2023, 10, 15),
     schedule='@daily'
)

def hello_world_etl():

    @task(multiple_outputs=True)    # to get in multiple parameters into get_name()
    def get_name():
        return {
            'first_name': 'Emmanuel' ,
            'last_name': 'Oyekanlu'
        }
    
    @task
    def get_age():
        return 4
    
    @task
    def greet(first_name, last_name, age ):
        print(f"Hello Programmer, my name is {first_name}, {last_name} and I am {age} years old")

    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'],
          last_name=name_dict['last_name'],
            age=age)

greet_dag = hello_world_etl()
    
