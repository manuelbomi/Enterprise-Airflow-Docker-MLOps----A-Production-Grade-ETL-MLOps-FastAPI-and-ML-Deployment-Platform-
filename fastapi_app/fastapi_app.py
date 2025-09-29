# Example usage 

# curl -X POST http://localhost:8000/trigger \
#   -H "Content-Type: application/json" \
#   -d '{"dag_id": "your_dag_id", "conf": {"param1": "value1"}}'

# http://localhost:8000/predict – for model inference.

# http://localhost:8000/trigger – to manually trigger Airflow DAGs.


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
import os
import httpx
from typing import Optional

# Base Airflow API URL and credentials
AIRFLOW_API_URL = os.environ.get("AIRFLOW_API_URL", "http://airflow-apiserver:8080/api/v1")
AIRFLOW_USERNAME = os.environ.get("AIRFLOW_USERNAME", "airflow")
AIRFLOW_PASSWORD = os.environ.get("AIRFLOW_PASSWORD", "airflow")

# Path to the deployed model
MODEL_PATH = "/tmp/production_model/model.pkl"

app = FastAPI(title="ML Model Prediction API")

# Input schema for prediction
class InputData(BaseModel):
    x: float

# Input schema for DAG trigger
class TriggerRequest(BaseModel):
    dag_id: str
    conf: Optional[dict] = {}

# Load model once at startup
model = None

@app.on_event("startup")
def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model not found at {MODEL_PATH}. Please deploy the model first.")
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

@app.post("/predict")
def predict(data: InputData):
    try:
        x_array = np.array([[data.x]])
        pred = model.predict(x_array)[0]
        return {"input": data.x, "prediction": pred}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/trigger")
async def trigger_dag(trigger_req: TriggerRequest):
    """
    Trigger an Airflow DAG run via the REST API.
    """
    url = f"{AIRFLOW_API_URL}/dags/{trigger_req.dag_id}/dagRuns"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json={"conf": trigger_req.conf},
                auth=(AIRFLOW_USERNAME, AIRFLOW_PASSWORD),
                timeout=10.0,
            )
        if response.status_code == 200:
            return {"message": f"DAG {trigger_req.dag_id} triggered successfully."}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
