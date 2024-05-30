from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class ruleDTO(BaseModel):
    ttype : Optional[str] = None
    description : Optional[str] = None
    transaction_group : Optional[str] = None
    transaction_type : Optional[str] = None
    vendor : Optional[str] = None
    customer : Optional[str] = None
    vendor_no_w9 : Optional[str] = None
    customer_no_w9 : Optional[str] = None
    class Config:
        orm_mode = True
    
class ruleFullDTO(BaseModel):
    id : Optional[int] = None
    ttype : Optional[str] = None
    description : Optional[str] = None
    transaction_group : Optional[str] = None
    transaction_type : Optional[str] = None
    vendor : Optional[str] = None
    customer : Optional[str] = None
    vendor_no_w9 : Optional[str] = None
    customer_no_w9 : Optional[str] = None
    class Config:
        orm_mode = True

class rulesListDTO(BaseModel):
    rules: List[ruleDTO]

class rulesFullListDTO(BaseModel):
    rules: List[ruleFullDTO]

class ruleDelDTO(BaseModel):
    ttype : Optional[str] = None
    description : Optional[str] = None

class rulesDelListDTO(BaseModel):
    rulesDel: List[ruleDelDTO]
    
class ruleQueryPrimaryKey(BaseModel):
    ttype: str = Field(None, description="Type of the rule to filter by")
    description: str = Field(None, description="Description of the rule to filter by")

class ruleQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists") 

RULES_COLUMNS = {
    'ttype': 'ttype',
    'description': 'description',
    'transaction_group': 'transaction_group',
    'transaction_type': 'transaction_type',
    'vendor': 'vendor',
    'customer': 'customer',
    'vendor_no_w9': 'vendor_no_w9',
    'customer_no_w9': 'customer_no_w9'
 }
    