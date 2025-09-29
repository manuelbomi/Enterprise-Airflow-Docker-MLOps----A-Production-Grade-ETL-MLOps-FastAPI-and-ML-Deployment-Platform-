# This is a lightweight test that confirms all DAGs in the /dags folder can be imported and parsed without error.
import os
from airflow.models import DagBag

def test_dags_import_without_errors():
    dag_bag = DagBag(dag_folder='dags', include_examples=False)

    assert len(dag_bag.import_errors) == 0, f"DAG import errors: {dag_bag.import_errors}"
