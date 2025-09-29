from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable, TaskInstance
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle
import os
import json

default_args = {
    'owner': 'mlops',
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

def ingest_data(ti: TaskInstance):
    data = pd.DataFrame({"x": np.random.rand(100)})
    data["y"] = 3 * data["x"] + np.random.randn(100) * 0.1
    ti.xcom_push(key="raw_data", value=data.to_json())

def preprocess_data(ti: TaskInstance):
    raw_data_json = ti.xcom_pull(key="raw_data", task_ids="ingest_data")
    df = pd.read_json(raw_data_json)
    X = df[["x"]]
    y = df["y"]
    ti.xcom_push(key="X", value=X.to_json())
    ti.xcom_push(key="y", value=y.to_json())

def train_model(ti: TaskInstance):
    X_json = ti.xcom_pull(key="X", task_ids="preprocess_data")
    y_json = ti.xcom_pull(key="y", task_ids="preprocess_data")
    X = pd.read_json(X_json)
    y = pd.read_json(y_json, typ="series")

    model = LinearRegression()
    model.fit(X, y)

    model_path = "/tmp/model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    ti.xcom_push(key="model_path", value=model_path)

def evaluate_model(ti: TaskInstance):
    model_path = ti.xcom_pull(key="model_path", task_ids="train_model")
    X_json = ti.xcom_pull(key="X", task_ids="preprocess_data")
    y_json = ti.xcom_pull(key="y", task_ids="preprocess_data")

    X = pd.read_json(X_json)
    y = pd.read_json(y_json, typ="series")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    preds = model.predict(X)
    mse = mean_squared_error(y, preds)
    print(f" Model MSE: {mse}")
    ti.xcom_push(key="mse", value=mse)

def register_model(ti: TaskInstance):
    model_path = ti.xcom_pull(key="model_path", task_ids="train_model")
    print(f" Model registered at: {model_path}")

# DAG Definition
with DAG(
    dag_id='ml_pipeline_python_operator_oyekanlu_v2',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['mlops', 'ml', 'training']
) as dag:

    task_ingest = PythonOperator(
        task_id='ingest_data',
        python_callable=ingest_data
    )

    task_preprocess = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data
    )

    task_train = PythonOperator(
        task_id='train_model',
        python_callable=train_model
    )

    task_evaluate = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model
    )

    task_register = PythonOperator(
        task_id='register_model',
        python_callable=register_model
    )

    # Set task dependencies
    task_ingest >> task_preprocess >> task_train >> task_evaluate >> task_register
