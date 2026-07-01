from sqlalchemy import ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class JobSummary(Base):
    __tablename__ = "job_summaries"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    job_id: Mapped[str] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    total_spend_inr: Mapped[float] = mapped_column(
        default=0
    )

    total_spend_usd: Mapped[float] = mapped_column(
        default=0
    )

    top_merchants: Mapped[dict] = mapped_column(
        JSON
    )

    category_breakdown: Mapped[dict] = mapped_column(
        JSON
    )

    anomaly_count: Mapped[int] = mapped_column(
        default=0
    )

    narrative: Mapped[str] = mapped_column(
        Text
    )

    risk_level: Mapped[str] = mapped_column(
        String(20)
    )

    job = relationship(
        "Job",
        back_populates="summary"
    )