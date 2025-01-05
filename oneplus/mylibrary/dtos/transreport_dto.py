from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class transreportDTO(BaseModel):
    sequence_id : Optional[int] = None
    category : Optional[str] = None
    calc_method : Optional[str] = None
    fields : Optional[str] = None
    class Config:
        from_attributes = True  

class transreportsListDTO(BaseModel):
    transreports: List[transreportDTO]

class transreportFullDTO(BaseModel):
    id : int
    sequence_id : Optional[int] = None
    category : Optional[str] = None
    calc_method : Optional[str] = None
    fields : Optional[str] = None
    class Config:
        from_attributes = True

class transreportsFullListDTO(BaseModel):
    transreports: List[transreportFullDTO]

class transreportDelDTO(BaseModel):
    sequence_id: Optional[int] = Field(None, description="Name of sequence id to filter by")

class transreportsDelListDTO(BaseModel):
    transreportsDel: List[transreportDelDTO]

class reportDTO(BaseModel):
    sequence_id : Optional[int] = None
    bank_account_key : Optional[str] = None
    category : Optional[str] = None
    month: Optional[str] = None
    amount: Optional[float] = None
    class Config:
        from_attributes = True  

class reportListDTO(BaseModel):
    performance: List[reportDTO]

class transreportQueryParams(BaseModel):
    sequence_id: Optional[int] = Field(None, description="Name of sequence id to filter by")
    category: Optional[str] = Field(None, description="Name of category to filter by")
    calc_method: Optional[str] = Field(None, description="Name of calc method to filter by")
    fields: Optional[str] = Field(None, description="Name of fields to filter by")
    
class transreportQueryPrimaryKey(BaseModel):
    sequence_id: Optional[int] = Field(None, description="Name of sequence id to filter by")

class reportQuery(BaseModel):
    bank_account_key: Optional[str] = Field(None, description="Name of bank_account to filter by")
    years: Optional[int] = Field(None, description="Number of years to filter by")

class transreportQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists") 

TRANSREPORT_COLUMNS = {
    'sequence_id': 'sequence_id',
    'category': 'category',
    'calc_method': 'calc_method',
    'fields': 'fields'
}
