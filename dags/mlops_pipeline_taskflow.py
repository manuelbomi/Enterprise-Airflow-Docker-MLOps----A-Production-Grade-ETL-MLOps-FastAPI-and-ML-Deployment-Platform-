# This module provides mlops using the fast and modern taskflow api method. 
# The FastAPI deployment is available at fastapi.py
# MLflow Tracking	Logs model + metrics to local URI (/tmp/mlruns)
# This module also provides: 
# - Validation Check	Fails the DAG if model performance is worse than baseline
# - Registry Logic	Simulated by saving models to /tmp/model_registry
# - Deployment Hook	Copies model to /tmp/production_model/model.pkl (for FastAPI use)
# - Monitoring	Stub for drift detection (can expand later)


# This module provides mlops using the fast and modern taskflow api method. 
# The FastAPI deployment is available at fastapi.py
# MLflow Tracking	Logs model + metrics to local URI (/tmp/mlruns)
# This module also provides: 
# - Validation Check	Fails the DAG if model performance is worse than baseline
# - Registry Logic	Simulated by saving models to /tmp/model_registry
# - Deployment Hook	Copies model to /tmp/production_model/model.pkl (for FastAPI use)
# - Monitoring	Stub for drift detection (can expand later)

from datetime import datetime
from airflow.decorators import dag, task
import pandas as pd
import numpy as np
import os
import pickle
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import json
import shutil

# -----------------------------
# Configurations & Constants
# -----------------------------
MLFLOW_TRACKING_URI = "file:///tmp/mlruns"
MODEL_REGISTRY_DIR = "/tmp/model_registry"
DEPLOYMENT_DIR = "/tmp/production_model"
BASELINE_MSE = 0.1

os.makedirs(MODEL_REGISTRY_DIR, exist_ok=True)
os.makedirs(DEPLOYMENT_DIR, exist_ok=True)

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# -----------------------------
# Define DAG
# -----------------------------
@dag(
    dag_id="mlops_pipeline_taskflow_emm_oye_v5",
    description="End-to-end MLOps pipeline with MLflow, validation, deployment, and monitoring",
    schedule='@daily',
    start_date=datetime(2025, 9, 28),
    catchup=False,
    tags=["mlops", "mlflow", "taskflow"]
)
def mlops_pipeline():

    @task
    def ingest_data():
        df = pd.DataFrame({
            "x": np.random.rand(100)
        })
        df["y"] = 3 * df["x"] + np.random.randn(100) * 0.1
        return df.to_json()

    @task
    def preprocess(data_json: str):
        df = pd.read_json(data_json)
        X = df[["x"]]
        y = df["y"]
        return {"X": X.to_json(), "y": y.to_json()}

    @task
    def train_model(X_json: str, y_json: str):
        X = pd.read_json(X_json)
        y = pd.read_json(y_json, typ="series")

        model = LinearRegression()
        model.fit(X, y)

        preds = model.predict(X)
        mse = mean_squared_error(y, preds)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        model_path = os.path.join(DEPLOYMENT_DIR, f"model_{timestamp}.pkl")

        with open(model_path, "wb") as f:
            pickle.dump(model, f)

        return json.dumps({
            "model_path": model_path,
            "mse": mse
        })

    @task
    def validate_model(train_output_json: str):
        data = json.loads(train_output_json)
        mse = data["mse"]
        if mse > BASELINE_MSE:
            raise ValueError(f"Validation failed: MSE {mse} is worse than baseline {BASELINE_MSE}")
        return train_output_json

    @task
    def register_model(validated_model_json: str):
        data = json.loads(validated_model_json)
        model_path = data["model_path"]
        mse = data["mse"]

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        with mlflow.start_run(run_name="mlops_pipeline_run") as run:
            mlflow.log_param("model_type", "LinearRegression")
            mlflow.log_metric("mse", mse)
            mlflow.sklearn.log_model(model, artifact_path="model")

            registered_model_path = os.path.join(MODEL_REGISTRY_DIR, os.path.basename(model_path))
            shutil.copy(model_path, registered_model_path)

        return registered_model_path

    @task
    def deploy_model(registered_model_path: str):
        deployed_path = os.path.join(DEPLOYMENT_DIR, "model.pkl")
        shutil.copy(registered_model_path, deployed_path)
        print(f"Model deployed to: {deployed_path}")
        return deployed_path

    @task
    def monitor_model(deployed_model_path: str):
        print(f"Monitoring model at {deployed_model_path}... (Simulated)")

    # -----------------------------
    # Task Chaining
    # -----------------------------
    raw_data = ingest_data()
    processed = preprocess(raw_data)
    trained = train_model(processed.get("X"), processed.get("y"))
    validated = validate_model(trained)
    registered = register_model(validated)
    deployed = deploy_model(registered)
    monitor_model(deployed)

# Instantiate the DAG
mlops_dag = mlops_pipeline()
