from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class cashflowDTO(BaseModel):
    bank_account_key : Optional[str] = None
    start_date : Optional[date] = None
    end_date : Optional[date] = None
    cash_change : Optional[float] = None
    ending_balance : Optional[float] = None
    calc_balance : Optional[float] = None
    period_status : Optional[str] = None
    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d'),
            float: lambda v: float('nan') if v in [float('inf'), float('-inf'), float('nan')] else v
        }

class cashflowsListDTO(BaseModel):
    cashflows: List[cashflowDTO]
   
class cashflowFullDTO(BaseModel):
    id : Optional[int] = None
    bank_account_key : Optional[str] = None
    start_date : Optional[date] = None
    end_date : Optional[date] = None
    cash_change : Optional[float] = None
    ending_balance : Optional[float] = None
    calc_balance : Optional[float] = None
    period_status : Optional[str] = None
    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d'),
            float: lambda v: float('nan') if v in [float('inf'), float('-inf'), float('nan')] else v
        }

class cashflowsFullListDTO(BaseModel):
    cashflows: List[cashflowFullDTO]

class cashflowDelDTO(BaseModel):
    bank_account_key : Optional[str] = None
    start_date : Optional[date] = None
    end_date : Optional[date] = None

class cashflowsDelListDTO(BaseModel):
    cashflowsDel: List[cashflowDelDTO]

class cashflowQueryParams(BaseModel):
    bank_account_key : Optional[str] = None
    start_date : Optional[date] = None
    end_date : Optional[date] = None
    cash_change : Optional[float] = None
    ending_balance : Optional[float] = None
    calc_balance : Optional[float] = None
    period_status : Optional[str] = None
    
class cashflowQueryPrimaryKey(BaseModel):
    bank_account_key : Optional[str] = None
    start_date : Optional[date] = None
    end_date : Optional[date] = None

class cashflowQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists") 


CASHFLOWS_COLUMNS = {
    'bank_account_key': 'bank_account_key',
    'start_date': 'start_date',
    'end_date': 'end_date',
    'cash_change': 'cash_change',
    'ending_balance': 'ending_balance',
    'calc_balance': 'calc_balance',
    'period_status': 'period_status'
}    