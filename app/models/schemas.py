from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel

from app.models.job import JobStatus


class JobCreate(BaseModel):
    task_type: str
    payload: dict[str, Any]


class JobResponse(BaseModel):
    id: UUID
    task_type: str
    payload: dict[str, Any]

    status: JobStatus

    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None

    retry_count: int = 0
    max_retries: int = 3

    error_message: str | None = None
    result: Any | None = None