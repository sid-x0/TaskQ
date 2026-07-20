from fastapi import APIRouter

from datetime import datetime
from uuid import uuid4

from app.core.queue import save_job, enqueue_job
from app.models.job import JobStatus
from app.models.schemas import JobCreate, JobResponse


router = APIRouter()


# @router.get("/test")
# def test():
#     return {
#         "message": "Routes are working!"
#     }
    
@router.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate):
    new_job = JobResponse(
        id=uuid4(),
        task_type=job.task_type,
        payload=job.payload,
        status=JobStatus.PENDING,
        created_at=datetime.now(),
        started_at=None,
        completed_at=None,
        retry_count=0,
        max_retries=3,
        error_message=None,
        result=None,
    )

    save_job(new_job)
    enqueue_job(str(new_job.id))

    return new_job