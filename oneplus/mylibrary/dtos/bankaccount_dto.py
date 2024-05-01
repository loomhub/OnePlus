from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class bankaccountDTO(BaseModel):
    bank : Optional[str] = None
    account_type : Optional[str] = None
    account_number : Optional[str] = None
    llc : Optional[str] = None
    property_name : Optional[str] = None
    class Config:
        orm_mode = True
    
    
class bankaccountFullDTO(BaseModel):
    id : Optional[int] = None
    bank : Optional[str] = None
    account_type : Optional[str] = None
    account_number : Optional[str] = None
    llc : Optional[str] = None
    property_name : Optional[str] = None
    class Config:
        orm_mode = True
    
class bankaccountsListDTO(BaseModel):
    bankaccounts: List[bankaccountDTO]

class bankaccountsFullListDTO(BaseModel):
    bankaccounts: List[bankaccountFullDTO]

class bankaccountDelDTO(BaseModel):
    bank: Optional[str] = Field(None, description="Name of the bankaccount to filter by")
    account_type: Optional[str] = Field(None, description="Name of the account type to filter by")
    account_number: Optional[str] = Field(None, description="Name of the account number to filter by")

class bankaccountsDelListDTO(BaseModel):
    bankaccountsDel: List[bankaccountDelDTO]

class bankaccountQueryParams(BaseModel):
    bank: Optional[str] = Field(None, description="Name of the bankaccount to filter by")
    account_type: Optional[str] = Field(None, description="Name of the account type to filter by")
    account_number: Optional[str] = Field(None, description="Name of the account number to filter by")

class bankaccountQueryPrimaryKey(BaseModel):
    bank: Optional[str] = Field(None, description="Name of the bankaccount to filter by")
    account_type: Optional[str] = Field(None, description="Name of the account type to filter by")
    account_number: Optional[str] = Field(None, description="Name of the account number to filter by")

class bankaccountQueryEmail(BaseModel):
    receiver: Optional[str] = Field(None, description="Name of the email receiver")


BANK_ACCOUNTS_COLUMNS = {
    'Bank': 'bank',
    'AccountType': 'account_type',
    'ExternalAccount': 'account_number',
    'LLC': 'llc',
    'Property': 'property_name'
}    