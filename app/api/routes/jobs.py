from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.job import UploadResponse
from app.services.jobs.job_service import JobService

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