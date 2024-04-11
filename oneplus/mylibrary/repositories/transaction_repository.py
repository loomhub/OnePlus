from sqlalchemy.orm import Session
from ..models.transaction_model import Transaction


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_transaction(self, transaction_id: int):
        return (
            self.db.query(Transaction).filter(Transaction.id == transaction_id).first()
        )

    def bulk_insert_transactions(self, db: Session, transactions_data: list):
        # Convert dicts to Transaction models
        transactions = [Transaction(**data) for data in transactions_data]

        db.bulk_save_objects(transactions)
        db.commit()
