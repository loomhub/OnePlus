from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.transaction_model import Transaction
from ..dtos.transaction_dto import TransactionCreate


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def insert_transaction(self, transaction: TransactionCreate):
        try:
            db_transaction = Transaction(
              date = transaction.date,
              description = transaction.description,
              details = transaction.details,
              amount = transaction.amount,
              classification = transaction.classification,
              asset = transaction.asset,
              transaction_group = transaction.transaction_group,
              transaction_type = transaction.transaction_type,
              vendor = transaction.vendor,
              customer = transaction.customer,
              comments = transaction.comments,
        )        
            self.db.add(db_transaction)
            self.db.commit()
            self.db.refresh(db_transaction)
            return db_transaction
        except Exception as e:
            raise HTTPException(status_code=402, detail=str(e))

#######################################################################

    def get_transaction(self, transaction_id: int):
        return (
            self.db.query(Transaction).filter(Transaction.id == transaction_id).first()
        )

    def bulk_insert_transactions(self, db: Session, transactions_data: list):
        # Convert dicts to Transaction models
        transactions = [Transaction(**data) for data in transactions_data]

        db.bulk_save_objects(transactions)
        db.commit()

    