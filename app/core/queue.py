from app.core.redis_client import redis_client
from app.models.schemas import JobResponse


def save_job(job: JobResponse):
    key = f"job:{job.id}"
    redis_client.set(key, job.model_dump_json())


def enqueue_job(job_id: str):
    redis_client.rpush("job_queue", job_id)


def get_job(job_id: str) -> JobResponse | None:
    key = f"job:{job_id}"

    data = redis_client.get(key)

    if data is None:
        return None

    return JobResponse.model_validate_json(data)


def dequeue_job():
    return redis_client.lpop("job_queue")