import time

from app.workers.celery_app import celery


@celery.task
def process_job(job_id: str):
    print(f"Processing Job {job_id}")

    time.sleep(5)

    print(f"Completed Job {job_id}")

    return True