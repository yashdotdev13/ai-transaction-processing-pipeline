
from uuid import uuid4

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.job_status import JobStatus
from app.db.base import Base

from datetime import datetime, timezone


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )

    filename: Mapped[str] = mapped_column(String(255), nullable=False)

    status: Mapped[str] = mapped_column(
        String(20),
        default=JobStatus.PENDING.value,
        nullable=False
    )

    row_count_raw: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    row_count_clean: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    completed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )

    error_message: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    transactions = relationship(
        "Transaction",
        back_populates="job",
        cascade="all, delete-orphan"
    )

    summary = relationship(
        "JobSummary",
        back_populates="job",
        uselist=False,
        cascade="all, delete-orphan"
    )