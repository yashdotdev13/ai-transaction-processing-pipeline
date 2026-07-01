from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.enums.job_status import JobStatus
from app.models.job import Job
from app.repositories.jobs.job_repository import JobRepository
from app.repositories.job_summary.job_summary_repository import JobSummaryRepository
from app.repositories.transactions.transaction_repository import TransactionRepository
from app.services.jobs.file_storage_service import FileStorageService
from app.workers.tasks import process_job


class JobService:

    @staticmethod
    def create_job(db: Session, file: UploadFile) -> Job:

        if not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=400,
                detail="Only CSV files are allowed."
            )

        job = Job(
            filename=file.filename,
            status=JobStatus.PENDING.value
        )

        job = JobRepository.create(db, job)

        FileStorageService.save(job.id, file)

        process_job.delay(str(job.id))

        return job

    @staticmethod
    def get_job_status(db: Session, job_id: str) -> Job:

        job = JobRepository.get_by_id(db, job_id)

        if job is None:
            raise HTTPException(
                status_code=404,
                detail="Job not found."
            )

        return job

    @staticmethod
    def get_job_results(db: Session, job_id: str):

        job = JobRepository.get_by_id(db, job_id)

        if job is None:
            raise HTTPException(
                status_code=404,
                detail="Job not found."
            )

        summary = JobSummaryRepository.get_by_job_id(
            db,
            job_id
        )

        transactions = TransactionRepository.get_by_job(
            db,
            job_id
        )

        return {
            "job": job,
            "summary": summary,
            "transactions": transactions,
        }