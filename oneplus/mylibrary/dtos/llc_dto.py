from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class llcDTO(BaseModel):
    llc : Optional[str] = None
    ein : Optional[str] = None
    llc_address : Optional[str] = None
    llc_description : Optional[str] = None
    formation_date : Optional[date] = None
    class Config:
        orm_mode = True  

class llcsListDTO(BaseModel):
    llcs: List[llcDTO]

class llcFullDTO(BaseModel):
    id : int
    llc : str
    ein : str
    llc_address : str 
    llc_description : str
    formation_date : date
    class Config:
        orm_mode = True

class llcsFullListDTO(BaseModel):
    llcs: List[llcFullDTO]

class llcDelDTO(BaseModel):
    llc : str

class llcsDelListDTO(BaseModel):
    llcsDel: List[llcDelDTO]

class LLCQueryParams(BaseModel):
    llc_name: Optional[str] = Field(None, description="Name of the LLC to filter by")
    start_date: Optional[date] = Field(None, description="Query LLCs created on or after this date")

class LLCQueryPrimaryKey(BaseModel):
    llc_name: str = Field(None, description="Name of the LLC to filter by")

class LLCQueryEmail(BaseModel):
    receiver: Optional[str] = Field(None, description="Name of the email receiver")

LLC_COLUMNS = {
    'LLC': 'llc',
    'EIN': 'ein',
    'Address': 'llc_address',
    'Description': 'llc_description',
    'FormationDate': 'formation_date'
}    