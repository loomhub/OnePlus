import pandas as pd
from ..repositories.transaction_repository import TransactionRepository
from ..database.db import get_db
from sqlalchemy.orm import Session


class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def get_transaction(self, transaction_id: int):
        return self.transaction_repository.get_transaction(transaction_id)

    @staticmethod
    def load_transactions_from_excel(db: Session, excel_file):
        df = pd.read_excel(excel_file.file, engine="openpyxl")

        transactions_data = df.to_dict(
            orient="records"
        )  # Converts DataFrame to list of dicts

        repository = TransactionRepository()
        repository.bulk_insert_transactions(db, transactions_data)
