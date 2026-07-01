from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    job_id: Mapped[str] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    txn_id: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    merchant: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    account_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    notes: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    is_anomaly: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    anomaly_reason: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    llm_category: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    llm_failed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    job = relationship(
        "Job",
        back_populates="transactions"
    )