from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class vendorDTO(BaseModel):
    vendor : Optional[str] = None
    recipient_type : Optional[str] = None
    recipient_tin_type : Optional[str] = None
    recipient_tin : Optional[str] = None
    last_name : Optional[str] = None
    first_name : Optional[str] = None
    address : Optional[str] = None
    city : Optional[str] = None
    state : Optional[str] = None
    zip_code : Optional[str] = None
    country : Optional[str] = None
    class Config:
        orm_mode = True
    
class vendorFullDTO(BaseModel):
    id : Optional[int] = None
    vendor : Optional[str] = None
    recipient_type : Optional[str] = None
    recipient_tin_type : Optional[str] = None
    recipient_tin : Optional[str] = None
    last_name : Optional[str] = None
    first_name : Optional[str] = None
    address : Optional[str] = None
    city : Optional[str] = None
    state : Optional[str] = None
    zip_code : Optional[str] = None
    country : Optional[str] = None
    class Config:
        orm_mode = True

class vendorsListDTO(BaseModel):
    vendors: List[vendorDTO]

class vendorsFullListDTO(BaseModel):
    vendors: List[vendorFullDTO]

class vendorDelDTO(BaseModel):
    vendor : Optional[str] = None

class vendorsDelListDTO(BaseModel):
    vendorsDel: List[vendorDelDTO]

class vendorQueryParams(BaseModel):
    vendor: Optional[str] = Field(None, description="Name of the vendor to filter by")
    
class vendorQueryPrimaryKey(BaseModel):
    vendor: Optional[str] = Field(None, description="Name of the LLC to filter by")

class vendorQueryEmail(BaseModel):
    receiver: Optional[str] = Field(None, description="Name of the email receiver")

class vendorQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists") 


VENDOR_COLUMNS = {
    'Vendor': 'vendor',
    'Recipient Type': 'recipient_type',
    'Recipient TIN Type': 'recipient_tin_type',
    'Recipent TIN': 'recipient_tin',
    'R Business Name or Last Name': 'last_name',
    'R First Name': 'first_name',
    'R Address 1': 'address',
    'R City': 'city',
    'R State': 'state',
    'R Zip Code': 'zip_code',
    'R Country': 'country'
}