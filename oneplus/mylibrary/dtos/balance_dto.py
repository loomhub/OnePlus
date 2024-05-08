from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class balanceDTO(BaseModel):
    bank_account_key : Optional[str] = None
    snapshot : Optional[date] = None
    balance : Optional[float] = None
    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d'),
            float: lambda v: float('nan') if v in [float('inf'), float('-inf'), float('nan')] else v
        }
   
class balanceFullDTO(BaseModel):
    bank_account_key : Optional[str] = None
    snapshot : Optional[date] = None
    balance : Optional[float] = None
    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d'),
            float: lambda v: float('nan') if v in [float('inf'), float('-inf'), float('nan')] else v
        }

class balancesListDTO(BaseModel):
    balances: List[balanceDTO]

class balancesFullListDTO(BaseModel):
    balances: List[balanceFullDTO]

class balanceDelDTO(BaseModel):
    bank_account_key : Optional[str] = None
    snapshot : Optional[date] = None

class balancesDelListDTO(BaseModel):
    balancesDel: List[balanceDelDTO]

class balanceQueryParams(BaseModel):
    bank_account_key : Optional[str] = None
    snapshot : Optional[date] = None
    
class balanceQueryPrimaryKey(BaseModel):
    bank_account_key : Optional[str] = None
    snapshot : Optional[date] = None

class balanceQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists") 


BALANCES_COLUMNS = {
    'Property': 'bank_account_key',
    'Month': 'snapshot',
    'Balance': 'balance'
    
}    