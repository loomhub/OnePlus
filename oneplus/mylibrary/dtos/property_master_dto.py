from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd

class propertyMasterDTO(BaseModel):
    property_name : Optional[str] = 'General'
    property_description : Optional[str] = 'General'
    llc : Optional[str] = 'LLC'
    note : Optional[str] = 'LLC'
    purchase_date : Optional[date] = date(1900,1,1)
    sell_date : Optional[date] = date(1900,1,1)
    purchase_price : Optional[float] = 0
    sell_price : Optional[float] = 0
    units: Optional[int] = 0
    county: Optional[str] = 'General'
    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d') if v is not None else None,
            float: lambda v: v if isinstance(v, (int, float)) and not pd.isna(v) else None,
            pd.Timestamp: lambda v: v.strftime('%Y-%m-%d') if not pd.isna(v) else None
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
            date: lambda v: v.strftime('%Y-%m-%d') if v is not None else None,
            float: lambda v: v if isinstance(v, (int, float)) and not pd.isna(v) else None,
            pd.Timestamp: lambda v: v.strftime('%Y-%m-%d') if not pd.isna(v) else None
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
    