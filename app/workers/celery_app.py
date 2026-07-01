from celery import Celery
from app.core.config import settings

print("=" * 60)
print("REDIS URL =", settings.REDIS_URL)
print("=" * 60)

celery = Celery(
    "transaction_pipeline",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)