#  Airflow TaskFlow API ML Pipeline Example
# How it works:
# Each @task is a Python function turned into a task node in the DAG.
# Data is passed automatically using XComs (here, JSON strings for portability).
# You can view task dependencies and logs in the Airflow UI.
from datetime import datetime
from airflow.decorators import dag, task
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle
import os
from io import StringIO




@dag(dag_id='ml_with_taskflow_v1',
    schedule='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["ml", "taskflow", "example"],
)
def ml_pipeline_taskflow():

    @task
    def ingest_data() -> str:
        # Generate synthetic data
        data = pd.DataFrame({
            "x": np.random.rand(100),
        })
        data["y"] = 3 * data["x"] + np.random.randn(100) * 0.1
        return data.to_json()

    @task
    def preprocess_data(data_json: str) -> tuple:
        df = pd.read_json(StringIO(data_json))
        X_json = df[["x"]].to_json()
        y_json = df["y"].to_json()
        return (X_json, y_json)

    @task
    def train_model(X_json: str, y_json: str) -> str:
        X = pd.read_json(StringIO(X_json))
        y = pd.read_json(StringIO(y_json), typ="series")

        model = LinearRegression()
        model.fit(X, y)

        model_path = "/tmp/model.pkl"
        with open(model_path, "wb") as f:
            pickle.dump(model, f)

        print(f"Model trained and saved to: {model_path}")
        return model_path

    @task
    def evaluate_model(model_path: str, X_json: str, y_json: str) -> float:
        X = pd.read_json(StringIO(X_json))
        y = pd.read_json(StringIO(y_json), typ="series")

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        preds = model.predict(X)
        mse = mean_squared_error(y, preds)
        print(f"Model MSE: {mse:.4f}")
        return mse

    @task
    def register_model(model_path: str):
        # Simulate model registration
        print(f"Model registered at path: {model_path}")

    # Task chaining
    raw_data = ingest_data()
    X_json, y_json = preprocess_data(raw_data)
    model_path = train_model(X_json, y_json)
    evaluate_model(model_path, X_json, y_json)
    register_model(model_path)

# Instantiate the DAG
ml_pipeline_taskflow_dag = ml_pipeline_taskflow()
