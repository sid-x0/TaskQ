from typing import Any
from pydantic import BaseModel


class JobCreate(BaseModel):
    task_type: str
    payload: dict[str, Any]