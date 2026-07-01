from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class TransactionRepository:

    @staticmethod
    def create(db: Session, transaction: Transaction):
        db.add(transaction)
        db.flush()
        return transaction

    @staticmethod
    def create_many(db: Session, transactions: list[Transaction]):
        db.add_all(transactions)

    @staticmethod
    def get_by_job(db: Session, job_id: str):
        return (
            db.query(Transaction)
            .filter(Transaction.job_id == job_id)
            .all()
        )