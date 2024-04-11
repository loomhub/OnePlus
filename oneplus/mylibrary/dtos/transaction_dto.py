from pydantic import BaseModel
from datetime import date


class TransactionDTO(BaseModel):
    id: int
    amount: float
    transaction_type: str
    account_id: int
    date: date
