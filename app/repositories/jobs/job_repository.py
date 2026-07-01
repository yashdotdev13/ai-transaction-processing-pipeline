from sqlalchemy.orm import Session

from app.models.job import Job


class JobRepository:

    @staticmethod
    def create(db: Session, job: Job):
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    @staticmethod
    def get_by_id(db: Session, job_id: str):
        return (
            db.query(Job)
            .filter(Job.id == job_id)
            .first()
        )


    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Job)
            .order_by(Job.created_at.desc())
            .all()
        )

    @staticmethod
    def get_by_status(db: Session, status: str):
        return (
            db.query(Job)
            .filter(Job.status == status)
            .order_by(Job.created_at.desc())
            .all()
        )