from datetime import datetime

from pydantic import BaseModel


class TransactionResult(BaseModel):
    txn_id: str | None
    date: datetime
    merchant: str
    amount: float
    currency: str
    status: str
    category: str | None
    llm_category: str | None
    is_anomaly: bool
    anomaly_reason: str | None

    model_config = {
        "from_attributes": True
    }


class JobSummaryResult(BaseModel):
    total_spend_inr: float
    total_spend_usd: float
    top_merchants: dict
    category_breakdown: dict
    anomaly_count: int
    narrative: str
    risk_level: str

    model_config = {
        "from_attributes": True
    }


class JobResultResponse(BaseModel):
    job_id: str
    filename: str
    status: str
    row_count_raw: int | None
    row_count_clean: int | None

    summary: JobSummaryResult

    transactions: list[TransactionResult]