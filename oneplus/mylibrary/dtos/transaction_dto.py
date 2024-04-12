from pydantic import BaseModel
from datetime import date


class TransactionDTO(BaseModel):
    date: date
    description: str
    details: str
    amount: float
    classification: str
    property_name: str
    transaction_group: str
    transaction_type: str
    vendor: str
    customer: str
    comments: str

class TransactionCreate(TransactionDTO):
    pass

class TransactionGet(TransactionDTO):
    id: int
    created_at: date

    class Config:
        orm_mode = True
