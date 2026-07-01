from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.enums.job_status import JobStatus
from app.models.job import Job
from app.repositories.jobs.job_repository import JobRepository
from app.services.jobs.file_storage_service import FileStorageService

from app.workers.tasks import process_job


class JobService:

    @staticmethod
    def create_job(db: Session, file: UploadFile) -> Job:

        # Validate file
        if not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=400,
                detail="Only CSV files are allowed."
            )

        # Create Job
        job = Job(
            filename=file.filename,
            status=JobStatus.PENDING.value
        )

        # Save Job
        job = JobRepository.create(db, job)

        # Save uploaded file
        FileStorageService.save(job.id, file)

        # Send job to Celery
        process_job.delay(str(job.id))

        return job