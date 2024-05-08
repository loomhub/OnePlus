from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class transactionTypeDTO(BaseModel):
    transaction_group : Optional[str] = None
    transaction_type : Optional[str] = None
    transaction_description : Optional[str] = None
    class Config:
        orm_mode = True
    
class transactionTypeFullDTO(BaseModel):
    id : Optional[int] = None
    transaction_group : Optional[str] = None
    transaction_type : Optional[str] = None
    transaction_description : Optional[str] = None
    class Config:
        orm_mode = True

class transactionTypesListDTO(BaseModel):
    transactionTypes: List[transactionTypeDTO]

class transactionTypesFullListDTO(BaseModel):
    transactionTypes: List[transactionTypeFullDTO]

class transactionTypeDelDTO(BaseModel):
    transaction_group: Optional[str] = Field(None, description="Name of the transactionGroup to filter by")
    transaction_type: Optional[str] = Field(None, description="Name of the transactionType to filter by")

class transactionTypesDelListDTO(BaseModel):
    transactionTypesDel: List[transactionTypeDelDTO]

class transactionTypeQueryParams(BaseModel):
    transaction_group: Optional[str] = Field(None, description="Name of the transactionGroup to filter by")
    transaction_type: Optional[str] = Field(None, description="Name of the transactionType to filter by")
    
class transactionTypeQueryPrimaryKey(BaseModel):
    transaction_group: Optional[str] = Field(None, description="Name of the transactionGroup to filter by")
    transaction_type: Optional[str] = Field(None, description="Name of the transactionType to filter by")

class transactionTypeQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists") 


TRANSACTION_TYPES_COLUMNS = {
    'Transaction Group': 'transaction_group',
    'Transaction Type': 'transaction_type',
    'Description': 'transaction_description'
}    