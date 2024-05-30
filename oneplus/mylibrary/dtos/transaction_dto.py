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

class transactionsListDTO(BaseModel):
    transactions: List[transactionDTO]
    
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

class transactionsFullListDTO(BaseModel):
    transactions: List[transactionFullDTO]

class transactionDelDTO(BaseModel):
    bank_account_key: Optional[str] = Field(None, description="Name of the bankaccount to filter by")
    tdate: Optional[date] = Field(None, description="Date of the transaction to filter by")
    description: Optional[str] = Field(None, description="Description of the transaction to filter by")
    amount: Optional[float] = Field(None, description="Amount of the transaction to filter by")

class transactionsDelListDTO(BaseModel):
    transactionsDel: List[transactionDelDTO]

class transactionSearchQuery(BaseModel):
    start_date: Optional[date] = Field(None, description="Start date for transaction date range")
    end_date: Optional[date] = Field(None, description="End date for transaction date range")
    min_amount: Optional[float] = Field(None, description="Minimum amount for transaction amount range")
    max_amount: Optional[float] = Field(None, description="Maximum amount for transaction amount range")
    classification: Optional[str] = Field(None, description="Classification of the transaction to filter by")
    transaction_group: Optional[str] = Field(None, description="Transaction group to filter by")
    transaction_type: Optional[str] = Field(None, description="Transaction type to filter by")
    description: Optional[str] = Field(None, description="Description of the transaction to filter by")
    vendor: Optional[str] = Field(None, description="Vendor of the transaction to filter by")
    customer: Optional[str] = Field(None, description="Customer of the transaction to filter by")
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists")
    
class transactionQueryPrimaryKey(BaseModel):
    bank_account_key: Optional[str] = Field(None, description="Name of the bankaccount to filter by")
    tdate: Optional[date] = Field(None, description="Date of the transaction to filter by")
    description: Optional[str] = Field(None, description="Description of the transaction to filter by")
    amount: Optional[float] = Field(None, description="Amount of the transaction to filter by")


class transactionQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists") 

TRANSACTIONS_COLUMNS = {
    'bank_account_key': 'bank_account_key',
    'tdate': 'tdate',
    'description': 'description',
    'amount': 'amount',
    'classification': 'classification',
    'period_status': 'period_status',
    'transaction_group': 'transaction_group',
    'transaction_type': 'transaction_type',
    'vendor': 'vendor',
    'customer': 'customer',
    'comments': 'comments',
    'vendor_no_w9': 'vendor_no_w9',
    'customer_no_w9': 'customer_no_w9',
    'Name': 'not_required1',
    'Notes': 'not_required2',
    'Category': 'not_required3',
    'Property': 'not_required4',
    'BankAccount': 'not_required5',
    'LLC': 'not_required6',
    'Note': 'not_required7',
    'Group': 'not_required8',
    'KeyCategory': 'not_required9',
    'W9Vendor': 'not_required10',
    'W9Customer': 'not_required11',
    'PropertyAddress': 'not_required12',
    'AccountType': 'not_required13',
    'Absolute': 'not_required14',
    'Year' : 'not_required15',
    'Month' : 'not_required16'
}

 