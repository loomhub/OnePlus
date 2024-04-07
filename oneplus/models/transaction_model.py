from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class BankTransaction(BaseModel):
    id: int
    amount: float
    date: datetime
    transaction_type: Literal['deposit', 'withdrawal']