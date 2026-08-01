import time

from app.core.queue import dequeue_job, get_job

print(" Worker started...")

while True:
    job_id = dequeue_job()

    if job_id is None:
        time.sleep(1)
        continue

    job = get_job(job_id)

    if job is None:
        print(f"Job {job_id} not found!")
        continue

    print("\n========================")
    print(f"Received Job")
    print(f"ID      : {job.id}")
    print(f"Task    : {job.task_type}")
    print(f"Payload : {job.payload}")
    print(f"Status  : {job.status}")
    print("========================\n")