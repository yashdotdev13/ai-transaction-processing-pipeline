from datetime import datetime
from pathlib import Path

from app.core.config import settings
from app.core.enums.job_status import JobStatus
from app.db.session import SessionLocal
from app.models.transaction import Transaction
from app.repositories.jobs.job_repository import JobRepository
from app.services.cleaning.csv_processor import CSVProcessor
from app.services.cleaning.data_cleaner import DataCleaner
from app.services.anomaly.anomaly_detector import AnomalyDetector
from app.services.ai.llm_categorizer import LLMCategorizer
from app.workers.celery_app import celery


job_repository = JobRepository()
csv_processor = CSVProcessor()
data_cleaner = DataCleaner()
anomaly_detector = AnomalyDetector()
llm_categorizer = LLMCategorizer()


@celery.task
def process_job(job_id: str):
    db = SessionLocal()

    try:
        print(f"\n========== Processing Job {job_id} ==========\n")

        # Fetch Job
        job = job_repository.get_by_id(db, job_id)

        if job is None:
            print("Job not found!")
            return False

        # CSV File Path
        file_path = Path(settings.UPLOAD_DIR) / job.id / job.filename

        print(f"CSV Path : {file_path}")

        # Read CSV
        df = csv_processor.process(str(file_path))

        raw_rows = len(df)

        # Clean Data
        df = data_cleaner.clean(df)

        # Detect anomalies
        df = anomaly_detector.detect(df)

        # Extract unique merchants
        unique_merchants = (
            df["merchant"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        print(f"Unique Merchants : {len(unique_merchants)}")

        merchant_categories = llm_categorizer.categorize_merchants(
            unique_merchants
        )

        print(merchant_categories)

        clean_rows = len(df)

        print(f"Raw Rows   : {raw_rows}")
        print(f"Clean Rows : {clean_rows}")

        # ==========================================
        # Save Transactions
        # ==========================================

        for _, row in df.iterrows():

            original_category = (
                None
                if row["category"] != row["category"]
                else str(row["category"])
            )

            notes = (
                ""
                if row["notes"] != row["notes"]
                else str(row["notes"])
            )

            # AI Categorization
            merchant = str(row["merchant"]).strip()

            llm_category = merchant_categories.get(
                merchant,
                original_category or "Other"
            )

            llm_failed = merchant not in merchant_categories

            print(
                f"{merchant:<20}"
                f"CSV={original_category} | "
                f"LLM={llm_category}"
            )

            transaction = Transaction(
                job_id=job.id,
                txn_id=str(row["txn_id"]),
                date=row["date"].to_pydatetime(),
                merchant=str(row["merchant"]),
                amount=float(row["amount"]),
                currency=str(row["currency"]),
                status=str(row["status"]),
                category=original_category,
                account_id=str(row["account_id"]),
                notes=notes,

                # Rule-based anomaly detection
                is_anomaly=bool(row["is_anomaly"]),
                anomaly_reason=(
                    str(row["anomaly_reason"])
                    if row["is_anomaly"]
                    else None
                ),

                # AI fields
                llm_category=llm_category,
                llm_failed=llm_failed,
            )

            db.add(transaction)

        print(f"\nSaved {clean_rows} transactions.")

        anomaly_count = int(df["is_anomaly"].sum())

        print(f"Anomalies Found : {anomaly_count}")

        # Update Job
        job.row_count_raw = raw_rows
        job.row_count_clean = clean_rows
        job.status = JobStatus.COMPLETED.value
        job.completed_at = datetime.utcnow()

        db.commit()

        print("\n========== JOB COMPLETED ==========\n")

        return True

    except Exception as e:

        db.rollback()

        if job is not None:
            job.status = JobStatus.FAILED.value
            job.error_message = str(e)
            db.commit()

        print(f"\nERROR: {e}\n")
        raise

    finally:
        db.close()