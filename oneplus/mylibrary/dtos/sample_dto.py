from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class sampleDTO(BaseModel):
    llc : Optional[str] = None
    ein : Optional[str] = None
    class Config:
        orm_mode = True
    
class sampleFullDTO(BaseModel):
    id : Optional[int] = None
    llc : Optional[str] = None
    ein : Optional[str] = None
    class Config:
        orm_mode = True

class samplesFullListDTO(BaseModel):
    samples: List[sampleFullDTO]

class sampleDelDTO(BaseModel):
    llc : Optional[str] = None

class samplesListDTO(BaseModel):
    samples: List[sampleDTO]

class samplesDelListDTO(BaseModel):
    samplesDel: List[sampleDelDTO]

class sampleQueryParams(BaseModel):
    sample: Optional[str] = Field(None, description="Name of the sample to filter by")
    
class sampleQueryPrimaryKey(BaseModel):
    sample: Optional[str] = Field(None, description="Name of the LLC to filter by")

SAMPLE_COLUMNS = {
    'LLC': 'llc',
    'EIN': 'ein',
    'Address': 'llc_address',
    'Description': 'llc_description',
    'FormationDate': 'formation_date'
}    