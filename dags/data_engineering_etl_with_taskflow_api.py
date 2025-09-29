# Use Case: ETL Pipeline Example Using TaskFlow API
# This example simulates:
# Extract: Fetching sales data (mocked as a random Pandas DataFrame)
# Transform: Cleaning and aggregating data
# Load: Saving the result to a local CSV file (simulating load to warehouse)


from airflow.decorators import dag, task
from datetime import datetime
import pandas as pd
import numpy as np
from io import StringIO

@dag(
    dag_id="etl_pipeline_taskflow_v4",
    description="ETL pipeline using TaskFlow API: extract -> transform -> load",
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["etl", "taskflow", "data-engineering"],
)
def etl_pipeline():

    @task
    def extract() -> str:
        print("Extracting data...")
        data = pd.DataFrame({
            'date': pd.date_range(start='2023-01-01', periods=10),
            'sales': np.random.randint(100, 1000, size=10)
        })
        return data.to_json()

    @task
    def transform(data_json: str) -> str:
        print("Transforming data...")
        df = pd.read_json(StringIO(data_json))  # fix warning

        df['date'] = pd.to_datetime(df['date'])
        df['sales'] = df['sales'].astype(int)

        df['month'] = df['date'].dt.to_period('M').astype(str)  # ✅ FIXED

        numeric_cols = df.select_dtypes(include='number').columns
        aggregated = df.groupby('month')[numeric_cols].sum().reset_index()

        print(f"Transformed Data:\n{aggregated}")
        return aggregated.to_json()

    @task
    def load(aggregated_json: str):
        print("Loading data...")
        df = pd.read_json(StringIO(aggregated_json))  # fix warning
        output_path = "/tmp/aggregated_sales.csv"
        df.to_csv(output_path, index=False)
        print(f"Data loaded to: {output_path}")

    # Task chaining
    raw_data = extract()
    cleaned_data = transform(raw_data)
    load(cleaned_data)

etl_dag = etl_pipeline()
