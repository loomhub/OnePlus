import pandas as pd
from ..repositories.transaction_repository import TransactionRepository
from ..dtos.transaction_dto import TransactionCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException

class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def create_transaction(self, db: Session, transaction: TransactionCreate):
        try:
            return self.transaction_repository.insert_transaction(transaction)
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e)) 

    #######################################################################
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

    
    def create_sample_transactions(self, input_data, db: Session):
        pass
        # Array of json objects
        # sample_data = [
        #     {
        #         "date": "2024-01-01",
        #         "description": "Sample transaction 1",
        #         "details": "Sample details 1",
        #         "amount": 100.0,
        #         "classification": "Revenue",
        #         "property": "104Meadow",
        #         "transaction_group": "Rent",
        #         "transaction_type": "Rent",
        #         "vendor": "Tenant",
        #         "customer": "104Meadow",
        #         "comments": "Sample comments 1",
        #     },
        #     {
        #         "date": "2024-01-02",
        #         "description": "Sample transaction 2",
        #         "details": "Sample details 2",
        #         "amount": 200.0,
        #         "classification": "Expense",
        #         "property": "116Meadow",
        #         "transaction_group": "Maintenance",
        #         "transaction_type": "Maintenance",
        #         "vendor": "Vendor",
        #         "customer": "116Meadow",
        #         "comments": "Sample comments 2",
        #     },
        # ]