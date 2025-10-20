# Enterprise Airflow Docker MLOps: A Production Grade ETL, MLOps, FastAPI, and ML Deployment Platform

#### Enterprise Airflow Docker MLOps is a production-grade, modular platform that demonstrates how to orchestrate end-to-end data engineering and MLOps workflows using Apache Airflow (TaskFlow API), Docker, Airflow Xcom and FastAPI.

Designed with enterprise use cases in mind, this project showcases how to:

- Build and manage ETL pipelines for data transformation

- Automate machine learning model training, validation, and deployment

- Leverage CI/CD pipelines to enforce quality and maintain workflow integrity

- Enable real-time model inference via FastAPI

- Use Airflow’s advanced features like XCom, backfilling, catchup, and custom plugins

- Ensure model reliability through baseline validation, model versioning, and registry logic

* Whether your team is building AI/ML pipelines, automating data workflows, or deploying models in enterprise production environments, this project provides a battle-tested starting point that is extensible, containerized, and CI/CD-ready.

--- 

## Tech Stack  

- Airflow (TaskFlow API) – Workflow orchestration, ETL, ML pipelines

- FastAPI – High-performance model serving

- MLflow – Model tracking, registry, and metrics logging

- Scikit-learn – Training regression models

- Pandas/Numpy – Data transformation

- Docker + Docker Compose – Containerized orchestration of services

- GitHub Actions (CI/CD) – Continuous Integration & DAG validation

- XCom – Task-to-task communication in Airflow

- Production-grade design – Model registry, validation, deployment, monitoring hooks

---

## Project Structure  


```ruby
enterprise-airflow-docker-mlops/
│
├── dags/                        # Airflow DAGs (various examples)
│   ├── mlops_pipeline_taskflow.py
│   ├── ml_pipeline_with_taskflow_api.py
│   ├── data_engineering_etl_with_taskflow_api.py
│   ├── data_engineering_etl_pipeline.py
│   ├── dag_with_taskflow_api.py
│   ├── ml_pipeline_with_traditional_dag.py
│   ├── dags_with_catchup_and_backfill.py
│   └── xcom_dag.py
│
├── fastapi_app/
│   ├── fastapi_app.py           # Model inference API
│   └── Dockerfile               # Optional: Standalone FastAPI Dockerfile
│
├── .github/workflows/
│   └── ci.yml                   # DAG validation, test automation
│
├── config/                      # (Optional) Airflow/ML configs
├── logs/                        # Airflow logs
├── models/                      # Persisted production models (served by FastAPI)
├── plugins/                     # Custom plugins, sensors, operators
├── project_snapshots/          # Snapshots of data/models
├── test/                        # Unit tests (DAGs, FastAPI, ML)
│   ├── test_dags.py
│   ├── test_fastapi.py
│   └── test_model.py
│
├── .gitignore
├── docker-compose.yaml          # Compose file for running the full system
├── Dockerfile.airflow           # Custom Airflow image
└── README.md                    # You are currently here! 


```
---

## Key Features 

 - TaskFlow API: Simplifies DAG writing using Python-native functions and decorators

 - ETL Pipelines: Easily build data engineering workflows with Airflow

-  ML Pipelines: End-to-end training, validation, and registration with MLflow

- MLOps Support: Baseline validation, model versioning, monitoring, and registry

- XCom Communication: Task-to-task data passing using native Airflow constructs

-  FastAPI Serving: Serve models via REST endpoint (http://localhost:8000)

-  CI/CD with GitHub Actions: DAG validation, linting, testing on push/PR

- Docker-based Orchestration: Easy spin-up of Airflow, Scheduler, UI, and FastAPI

- Production-Ready Hooks: Deployment logic, model monitoring stubs, custom registry

- Pluggable Architecture: Easily extendable via plugins, sensors, hooks

---


## Use Cases

Use this project as a blueprint for building real-world, enterprise-grade pipelines:

### Data Engineering & ETL  

- Build extract-transform-load (ETL) workflows using Airflow DAGs

- Use both traditional and TaskFlow API styles

- Backfill historical data using Airflow's catchup feature

### Machine Learning Pipelines  

- Train and validate ML models (e.g., Linear Regression)

- Log metrics and models to MLflow

- Register and version models

### MLOps – End-to-End Lifecycle 

- Validate model performance with production baseline (auto-fails DAG if worse)

- Register models to a simulated model registry

- Deploy best model to production (via FastAPI)

- Stub in for model monitoring and drift detection

### Model Deployment  

- Automatically deploy latest validated model to /models/model.pkl

- FastAPI reads this for real-time predictions

### FastAPI Inference API  

- Live at http://localhost:8000

- Sample endpoints:
  
    - GET / — Health check

    - POST /predict — Send JSON input for predictions
      
      ```ruby
      curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" \
      -d '{"x": 0.85}'        
      ```


### CI/CD Pipeline 

- GitHub Actions workflow in .github/workflows/ci.yml

- Runs on PR and push:
  
      - DAG validation

      - Linting

      - Unit tests for ML and API

- Ready to extend with deployment hooks
    



--- 

## How to Deploy for Your Enterprise Application

### 1. Clone the Repo  

      
```ruby
git clone https://github.com/manuelbomi/Enterprise-Airflow-Docker-MLOps----A-Production-Grade-ETL-MLOps-FastAPI-and-ML-Deployment-Platform-/tree/main
cd enterprise-airflow-docker-mlops

```

### 2. Build & Run with Docker Compose️

####  Build custom images

```ruby
docker compose build
```

#### Spin up the full stack: Airflow + FastAPI

```ruby
docker compose up
```

#### Visit  :  

<ins>Airflow UI</ins>: http://localhost:8080

<ins>FastAPI Server</ins>: http://localhost:8000



### 3. Run Your First DAG  

    - Go to Airflow UI: http://localhost:8080
    
    - Unpause mlops_pipeline_taskflow_emm_oye_v3

    - Trigger DAG manually or wait for the scheduler



#### FastAPI Endpoint Details    


| Method | Route      | Description                                                  |
|--------|------------|--------------------------------------------------------------|
| GET    | `/`        | Health check                                                 |
| POST   | `/predict` | Accepts JSON like `{"x": 0.5}` and returns model prediction  |


### 4. Running Tests

#### Run unit tests


```ruby
pytest test/

```

### 5.GitHub Actions (CI/CD)  

* CI/CD workflow automatically:

    - Validates all DAGs

    - Runs unit tests

    -  Lints code (expandable)

    -  Blocks merging broken DAGs

* File: .github/workflows/ci.yml

---

## Extending the Platform   

* You can use this project as a template to build:

     - Production-grade data pipelines

     - MLOps workflows with real monitoring

     - Automated ML retraining & deployment

     - Data validation + data drift detection

     - Full ML/ETL lifecycle orchestration
 
 ---

## Notes  

     - Models are saved in /tmp/production_model/model.pkl (shared with FastAPI)

     - MLflow runs are saved locally at /tmp/mlruns

     - Model validation uses MSE vs a BASELINE_MSE

     - All DAGs are Pythonic, modular, and reusable

     - Improvements are also welcome (submit a PR or clone and redeploy after citing this repo)

---

## License

MIT – Use freely in your enterprise environment!



---


Thank you for reading
  

### **AUTHOR'S BACKGROUND**
### Author's Name:  Emmanuel Oyekanlu
```
Skillset:   I have experience spanning several years in data science, developing scalable enterprise data pipelines,
enterprise solution architecture, architecting enterprise systems data and AI applications,
software and AI solution design and deployments, data engineering, high performance computing (GPU, CUDA), IoT applications,
machine learning, MLOps, NLP, Agentic-AI and LLM applications as well as deploying scalable solutions (apps) on-prem and in the cloud.

I can be reached through: manuelbomi@yahoo.com

Websites (professional):  http://emmanueloyekanlu.com/
Websites (application):  https://app.emmanueloyekanluprojects.com/
Publications:  https://scholar.google.com/citations?user=S-jTMfkAAAAJ&hl=en
LinkedIn:  https://www.linkedin.com/in/emmanuel-oyekanlu-6ba98616
Github:  https://github.com/manuelbomi

```
[![Icons](https://skillicons.dev/icons?i=aws,azure,gcp,scala,mongodb,redis,cassandra,kafka,anaconda,matlab,nodejs,django,py,c,anaconda,git,github,mysql,docker,kubernetes&theme=dark)](https://skillicons.dev)




  







