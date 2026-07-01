from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.job import (
    UploadResponse,
    JobStatusResponse,
)
from app.services.jobs.job_service import JobService
from app.schemas.result import JobResultResponse

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=201
)
def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    job = JobService.create_job(db, file)

    return UploadResponse(
        job_id=job.id,
        status=job.status,
        message="File uploaded successfully."
    )


@router.get(
    "/{job_id}/status",
    response_model=JobStatusResponse
)
def get_job_status(
    job_id: str,
    db: Session = Depends(get_db),
):

    job = JobService.get_job_status(
        db,
        job_id,
    )

    return JobStatusResponse(
        job_id=job.id,
        status=job.status,
        row_count_raw=job.row_count_raw,
        row_count_clean=job.row_count_clean,
        created_at=job.created_at,
        completed_at=job.completed_at,
        error_message=job.error_message,
    )

@router.get(
    "/{job_id}/results",
    response_model=JobResultResponse
)
def get_job_results(
    job_id: str,
    db: Session = Depends(get_db),
):

    result = JobService.get_job_results(
        db,
        job_id,
    )

    return JobResultResponse(
        job_id=result["job"].id,
        filename=result["job"].filename,
        status=result["job"].status,
        row_count_raw=result["job"].row_count_raw,
        row_count_clean=result["job"].row_count_clean,
        summary=result["summary"],
        transactions=result["transactions"],
    )