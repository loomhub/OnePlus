from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class emailConfigDTO(BaseModel):
    subject : Optional[str] = None
    endpoint : Optional[str] = None
    to : Optional[str] = None
    cc : Optional[str] = None
    bcc : Optional[str] = None
    inactive : Optional[str] = None
    class Config:
        orm_mode = True
    
class emailConfigFullDTO(BaseModel):
    id : Optional[int] = None
    subject : Optional[str] = None
    endpoint : Optional[str] = None
    to : Optional[str] = None
    cc : Optional[str] = None
    bcc : Optional[str] = None
    inactive : Optional[str] = None
    class Config:
        orm_mode = True

class emailsConfigFullListDTO(BaseModel):
    emailsConfig: List[emailConfigFullDTO]

class emailConfigDelDTO(BaseModel):
    subject : Optional[str] = None

class emailsConfigListDTO(BaseModel):
    emailsConfig: List[emailConfigDTO]

class emailsConfigDelListDTO(BaseModel):
    emailsConfigDel: List[emailConfigDelDTO]

class emailConfigQueryParams(BaseModel):
    subject: Optional[str] = Field(None, description="Name of the subject to filter by")
    endpoint: Optional[str] = Field(None, description="Name of the endpoint to filter by")
    
class emailConfigQueryPrimaryKey(BaseModel):
    subject: Optional[str] = Field(None, description="Name of the subject to filter by")

class emailConfigQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists") 

EMAIL_CONFIG_COLUMNS = {
    'Subject': 'subject',
    'Endpoint': 'endpoint',
    'To': 'to',
    'CC': 'cc',
    'BCC': 'bcc',
    'Inactive': 'inactive'  
}    