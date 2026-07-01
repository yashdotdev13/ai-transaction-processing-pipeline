from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.enums.job_status import JobStatus


class JobResponse(BaseModel):
    id: str
    filename: str
    status: JobStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class UploadResponse(BaseModel):
    job_id: str
    status: JobStatus
    message: str