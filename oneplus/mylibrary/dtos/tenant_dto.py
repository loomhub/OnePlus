from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class tenantDTO(BaseModel):
    customer : Optional[str] = None
    property_name : Optional[str] = None
    unit_name : Optional[str] = None
    lease_start : Optional[date] = None
    lease_end : Optional[date] = None
    rent : Optional[float] = None
    security_deposit : Optional[float] = None
    class Config:
        from_attributes = True
    
class tenantFullDTO(BaseModel):
    id : Optional[int] = None
    customer : Optional[str] = None
    property_name : Optional[str] = None
    unit_name : Optional[str] = None
    lease_start : Optional[date] = None
    lease_end : Optional[date] = None
    rent : Optional[float] = None
    security_deposit : Optional[float] = None
    class Config:
        from_attributes = True
    
class tenantsListDTO(BaseModel):
    tenants: List[tenantDTO]

class tenantsFullListDTO(BaseModel):
    tenants: List[tenantFullDTO]

class tenantDelDTO(BaseModel):
    customer : Optional[str] = None
    property_name : Optional[str] = None
    unit_name : Optional[str] = None
    lease_start : Optional[date] = None
    lease_end : Optional[date] = None

class tenantsDelListDTO(BaseModel):
    tenantsDel: List[tenantDelDTO]

class tenantQueryParams(BaseModel):
    customer: Optional[str] = Field(None, description="Name of the tenant to filter by")
    property_name: Optional[str] = Field(None, description="Name of the property to filter by")
    unit_name: Optional[str] = Field(None, description="Name of the unit to filter by")
    lease_start: Optional[date] = Field(None, description="Date of the lease start to filter by")
    lease_end: Optional[date] = Field(None, description="Date of the lease end to filter by")
    
class tenantQueryPrimaryKey(BaseModel):
    customer: Optional[str] = Field(None, description="Name of the tenant to filter by")
    property_name: Optional[str] = Field(None, description="Name of the property to filter by")
    unit_name: Optional[str] = Field(None, description="Name of the unit to filter by")
    lease_start: Optional[date] = Field(None, description="Date of the lease start to filter by")
    lease_end: Optional[date] = Field(None, description="Date of the lease end to filter by")

class tenantQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists") 


TENANTS_COLUMNS = {
    'Tenant': 'customer',
    'Property': 'property_name',
    'Unit': 'unit_name',
    'Lease Start': 'lease_start',
    'Lease End': 'lease_end',
    'Rent': 'rent',
    'Security Deposit': 'security_deposit'
}
