import time
from datetime import datetime

from app.core.queue import dequeue_job, get_job, save_job, enqueue_job, enqueue_dead_letter, heartbeat
from app.models.job import JobStatus
from app.tasks.sleep import execute
import uuid

worker_id = str( uuid.uuid4())

def send_heartbeat():
    while True:
        heartbeat( worker_id )
        time.sleep(5)
        
threading.thread(
    target = send_heartbeat,
    daemon = True
).start()

print(" Worker started...")

while True:
    
    heartbeat( worker_id )
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
        
        save_job(job)
    
        print(f"Completed job {job.id}")
        
        
    except Exception as e:
        print(f"Job {job.id} failed : {e}")
        
        
        #retry
        if job.retry_count < job.max_retries:
            
            job.retry_count += 1
            job.status = JobStatus.RETRYING
            job.error_message = str(e)
            
            save_job(job)
            
            delay = 2 **(job.retry_count - 1)
            
            print(
                f"Retrying job {job.id} "
                f"in {delay} sec"
                f"(attempt {job.retry_count}/{job.max_retries})"
            )
            
            time.sleep(delay)
            
            enqueue_job(job.id)
            
        else:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            
            save_job(job)
            
            enqueue_dead_letter(job.id)
            
            print(
                f"Job {job.id} permamnently failed "
                f"and moved to DLQ"
            )
        
