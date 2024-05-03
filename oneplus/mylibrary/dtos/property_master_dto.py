from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class propertyMasterDTO(BaseModel):
    property_name : Optional[str] = None
    property_description : Optional[str] = None
    llc : Optional[str] = None
    note : Optional[str] = None
    purchase_date : Optional[date] = None
    sell_date : Optional[date] = None
    purchase_price : Optional[float] = None
    sell_price : Optional[float] = None
    units: Optional[int] = None
    county: Optional[str] = None
    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d'),
            float: lambda v: float('nan') if v in [float('inf'), float('-inf'), float('nan')] else v
        }

class propertyMasterFullDTO(BaseModel):
    id : Optional[int] = None
    property_name : Optional[str] = None
    property_description : Optional[str] = None
    llc : Optional[str] = None
    note : Optional[str] = None
    purchase_date : Optional[date] = None
    sell_date : Optional[date] = None
    purchase_price : Optional[float] = None
    sell_price : Optional[float] = None
    units: Optional[int] = None
    county: Optional[str] = None
    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d'),
            float: lambda v: float('nan') if v in [float('inf'), float('-inf'), float('nan')] else v
        }

class propertyMastersListDTO(BaseModel):
    propertyMasters: List[propertyMasterDTO]

class propertyMastersFullListDTO(BaseModel):
    propertyMasters: List[propertyMasterFullDTO]

class propertyMasterDelDTO(BaseModel):
    property_name: Optional[str] = Field(None, description="Name of the property to filter by")

class propertyMastersDelListDTO(BaseModel):
    propertyMastersDel: List[propertyMasterDelDTO]

class propertyMasterQueryParams(BaseModel):
    property_name: Optional[str] = Field(None, description="Name of the property to filter by")
    
class propertyMasterQueryPrimaryKey(BaseModel):
    property_name: Optional[str] = Field(None, description="Name of the property to filter by")

class propertyMasterQueryEmail(BaseModel):
    receiver: Optional[str] = Field(None, description="Name of the email receiver")

class propertyMasterQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists") 


PROPERTY_MASTER_COLUMNS = {
    'Property': 'property_name',
    'Property Description': 'property_description',
    'LLC': 'llc',
    'Title': 'note',
    'Purchase Date': 'purchase_date',
    'Sell Date': 'sell_date',
    'Purchase Price': 'purchase_price',
    'Sell Price': 'sell_price',
    'Units': 'units',
    'County': 'county'
}
    