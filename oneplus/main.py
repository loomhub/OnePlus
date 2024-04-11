from fastapi import FastAPI
import uvicorn
from mylibrary.database.db import Base, get_db
from mylibrary.models.transaction_model import Transaction
from mylibrary.dtos.transaction_dto import TransactionDTO # 
from mylibrary.repositories.transaction_repository import TransactionRepository
from mylibrary.services.transaction_service import TransactionService # 
from mylibrary.controllers.transaction_controller import router as transactions_router # New import

app = FastAPI()
app.include_router(transactions_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
