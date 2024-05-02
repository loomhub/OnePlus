from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class transactionDTO(BaseModel):
    bank_account_key : Optional[str] = None
    tdate : Optional[date] = None
    description : Optional[str] = None
    amount : Optional[float] = None
    classification : Optional[str] = None
    period_status : Optional[str] = None
    transaction_group : Optional[str] = None
    transaction_type : Optional[str] = None
    vendor : Optional[str] = None
    customer : Optional[str] = None
    comments : Optional[str] = None
    vendor_no_w9 : Optional[str] = None
    customer_no_w9 : Optional[str] = None
    class Config:
        orm_mode = True
    
class transactionFullDTO(BaseModel):
    id : Optional[int] = None
    bank_account_key : Optional[str] = None
    tdate : Optional[date] = None
    description : Optional[str] = None
    amount : Optional[float] = None
    classification : Optional[str] = None
    period_status : Optional[str] = None
    transaction_group : Optional[str] = None
    transaction_type : Optional[str] = None
    vendor : Optional[str] = None
    customer : Optional[str] = None
    comments : Optional[str] = None
    vendor_no_w9 : Optional[str] = None
    customer_no_w9 : Optional[str] = None
    class Config:
        orm_mode = True

class transactionsListDTO(BaseModel):
    transactions: List[transactionDTO]

class transactionsFullListDTO(BaseModel):
    transactions: List[transactionFullDTO]

class transactionDelDTO(BaseModel):
    bank_account_key: Optional[str] = Field(None, description="Name of the bankaccount to filter by")
    tdate: Optional[date] = Field(None, description="Date of the transaction to filter by")
    description: Optional[str] = Field(None, description="Description of the transaction to filter by")
    amount: Optional[float] = Field(None, description="Amount of the transaction to filter by")

class transactionsDelListDTO(BaseModel):
    transactionsDel: List[transactionDelDTO]

class transactionQueryParams(BaseModel):
    bank_account_key: Optional[str] = Field(None, description="Name of the bankaccount to filter by")
    tdate: Optional[date] = Field(None, description="Date of the transaction to filter by")
    description: Optional[str] = Field(None, description="Description of the transaction to filter by")
    amount: Optional[float] = Field(None, description="Amount of the transaction to filter by")
    
    
class transactionQueryPrimaryKey(BaseModel):
    bank_account_key: Optional[str] = Field(None, description="Name of the bankaccount to filter by")
    tdate: Optional[date] = Field(None, description="Date of the transaction to filter by")
    description: Optional[str] = Field(None, description="Description of the transaction to filter by")
    amount: Optional[float] = Field(None, description="Amount of the transaction to filter by")
    
class transactionQueryEmail(BaseModel):
    receiver: Optional[str] = Field(None, description="Name of the email receiver")

class transactionQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists") 

TRANSACTIONS_COLUMNS = {
    'Bank Key': 'bank_account_key',
    'Date': 'tdate',
    'Description': 'description',
    'Amount': 'amount',
    'Classification': 'classification',
    'Period Status': 'period_status',
    'Group': 'transaction_group',
    'Type': 'transaction_type',
    'Vendor': 'vendor',
    'Customer': 'customer',
    'Comments': 'comments',
    'General Vendor': 'vendor_no_w9',
    'General Customer': 'customer_no_w9'
}

 