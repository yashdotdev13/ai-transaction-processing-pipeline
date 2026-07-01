from pathlib import Path
import shutil

from fastapi import UploadFile

from app.core.config import settings


class FileStorageService:

    @staticmethod
    def save(job_id: str, file: UploadFile) -> Path:
        upload_dir = Path(settings.UPLOAD_DIR) / job_id
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / file.filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path