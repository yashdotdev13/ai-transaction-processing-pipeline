from app.db.session import SessionLocal
from app.repositories.jobs.job_repository import JobRepository
from app.services.cleaning.csv_processor import CSVProcessor
from app.workers.celery_app import celery

from pathlib import Path
from app.core.config import settings

job_repository = JobRepository()
csv_processor = CSVProcessor()


@celery.task
def process_job(job_id: str):
    db = SessionLocal()

    try:
        print(f"\n========== Processing Job {job_id} ==========\n")

        # Fetch Job
        job = job_repository.get_by_id(db, job_id)

        if job is None:
            print("Job not found!")
            return False

        print(f"Job ID : {job.id}")

        file_path = Path(settings.UPLOAD_DIR) / job.id / job.filename

        print(f"CSV Path : {file_path}")

        df = csv_processor.process(str(file_path))

        print("\nCSV Loaded Successfully!\n")

        print(df.head())
        print(f"\nTotal Rows    : {len(df)}")
        print(f"Total Columns : {len(df.columns)}")

        print(f"\n========== Completed Job {job_id} ==========\n")

        return True

    except Exception as e:
        print(f"Error while processing job: {e}")
        raise

    finally:
        db.close()