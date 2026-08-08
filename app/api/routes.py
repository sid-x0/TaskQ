from fastapi import APIRouter, HTTPException

from datetime import datetime
from uuid import uuid4

from app.core.queue import save_job, enqueue_job, get_job
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

@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job_status(job_id: str):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job

