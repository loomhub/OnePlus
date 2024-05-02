from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class customerDTO(BaseModel):
    customer : Optional[str] = None
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
    
class customerFullDTO(BaseModel):
    id : Optional[int] = None
    customer : Optional[str] = None
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

class customersListDTO(BaseModel):
    customers: List[customerDTO]

class customersFullListDTO(BaseModel):
    customers: List[customerFullDTO]

class customerDelDTO(BaseModel):
    customer : Optional[str] = None

class customersDelListDTO(BaseModel):
    customersDel: List[customerDelDTO]

class customerQueryParams(BaseModel):
    customer: Optional[str] = Field(None, description="Name of the customer to filter by")
    
class customerQueryPrimaryKey(BaseModel):
    customer: Optional[str] = Field(None, description="Name of the LLC to filter by")

class customerQueryEmail(BaseModel):
    receiver: Optional[str] = Field(None, description="Name of the email receiver")

class customerQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists") 


CUSTOMER_COLUMNS = {
    'Customer': 'customer',
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