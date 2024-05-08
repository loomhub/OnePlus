from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class bankdownloadDTO(BaseModel):
    bank_account_key : Optional[str] = None
    tdate : Optional[date] = None
    description : Optional[str] = None
    amount : Optional[float] = None
    class Config:
        orm_mode = True
    
class bankdownloadFullDTO(BaseModel):
    id : Optional[int] = None
    bank_account_key : Optional[str] = None
    tdate : Optional[date] = None
    description : Optional[str] = None
    amount : Optional[float] = None
    class Config:
        orm_mode = True

class bankdownloadsListDTO(BaseModel):
    bankdownloads: List[bankdownloadDTO]

class bankdownloadsFullListDTO(BaseModel):
    bankdownloads: List[bankdownloadFullDTO]

class bankdownloadDelDTO(BaseModel):
    bank_account_key: Optional[str] = Field(None, description="Name of the bankdownload to filter by")
    tdate: Optional[date] = Field(None, description="Date of the bankdownload to filter by")
    description: Optional[str] = Field(None, description="Description of the bankdownload to filter by")
    amount: Optional[float] = Field(None, description="Amount of the bankdownload to filter by")

class bankdownloadsDelListDTO(BaseModel):
    bankdownloadsDel: List[bankdownloadDelDTO]

class bankdownloadQueryParams(BaseModel):
    bank_account_key: Optional[str] = Field(None, description="Name of the bankdownload to filter by")
    tdate: Optional[date] = Field(None, description="Date of the bankdownload to filter by")
    description: Optional[str] = Field(None, description="Description of the bankdownload to filter by")
    amount: Optional[float] = Field(None, description="Amount of the bankdownload to filter by")
    
class bankdownloadQueryPrimaryKey(BaseModel):
    bank_account_key: Optional[str] = Field(None, description="Name of the bankdownload to filter by")
    tdate: Optional[date] = Field(None, description="Date of the bankdownload to filter by")
    description: Optional[str] = Field(None, description="Description of the bankdownload to filter by")
    amount: Optional[float] = Field(None, description="Amount of the bankdownload to filter by")

class bankdownloadQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists") 

WELLSFARGO_FILEHEADERS = ['tdate','amount','not_required1','not_required2','description']

CHASE_COLUMNS = {
    'Details': 'not_required1',
    'Posting Date': 'tdate',
    'Description': 'description',
    'Amount': 'amount',
    'Type': 'not_required2',
    'Balance': 'not_required3',
    'Check or Slip #': 'not_required4'
}    
WELLSFARGO_COLUMNS = {
    'tdate': 'tdate',
    'amount': 'amount',
    'not_required1': 'not_required1',
    'not_required2': 'not_required2',
    'description': 'description'  
}    