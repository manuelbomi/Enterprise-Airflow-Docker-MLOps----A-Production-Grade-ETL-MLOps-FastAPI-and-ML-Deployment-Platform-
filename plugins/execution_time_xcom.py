from airflow.models.xcom import BaseXCom
from typing import Any
from sqlalchemy.engine import Row


class ExecutionTimeXCom(BaseXCom):
    @staticmethod
    def serialize_value(value: Any) -> Any:
        # You can customize this
        return super().serialize_value(value)

    @staticmethod
    def deserialize_value(result: Any) -> Any:
        # You can customize this
        return super().deserialize_value(result)
