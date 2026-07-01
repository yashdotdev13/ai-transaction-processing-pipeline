from sqlalchemy.orm import Session

from app.models.job_summary import JobSummary


class JobSummaryRepository:

    @staticmethod
    def create(db: Session, summary: JobSummary) -> JobSummary:
        db.add(summary)
        db.flush()
        return summary

    @staticmethod
    def get_by_job_id(db: Session, job_id: str):
        return (
            db.query(JobSummary)
            .filter(JobSummary.job_id == job_id)
            .first()
        )

    @staticmethod
    def update(db: Session, summary: JobSummary):
        db.add(summary)
        db.flush()
        return summary