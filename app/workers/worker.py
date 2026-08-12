import time
from datetime import datetime

from app.core.queue import dequeue_job, get_job, save_job
from app.models.job import JobStatus
from app.tasks.sleep import execute

print(" Worker started...")

while True:
    job_id = dequeue_job()

    if job_id is None:
        time.sleep(1)
        continue

    job = get_job(job_id)

    if job is None:
        continue
    
    #mark as runnign
    job.status = JobStatus.RUNNING
    job.started_at = datetime.now()
    save_job(job)
    
    print(f"▶ Executing job {job.id}...")
    
    try:
        if job.task_type == 'sleep':
            execute(job.payload)
            
        elif job.task_type == "fail":
            from app.tasks.fail import execute as fail_task
            fail_task(job.payload)
            
            
        #mark as completed
        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.now()
    
        print(f"Completed job {job.id}")
    except Exception as e:
        #task failed
        job.status = JobStatus.FAILED
        job.error_message = str(e)
        
        print(f"Jpb {job.id} failed: {e}")
        
    save_job(job)
