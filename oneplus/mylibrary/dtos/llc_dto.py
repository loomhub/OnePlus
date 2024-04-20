from datetime import date
from pydantic import BaseModel
from typing import List

class llcDTO(BaseModel):
    llc : str
    ein : str
    llc_address : str 
    llc_description : str
    formation_date : date

class llcFullDTO(BaseModel):
    id : int
    llc : str
    ein : str
    llc_address : str 
    llc_description : str
    formation_date : date
    class Config:
        orm_mode = True

class llcsListFullDTO(BaseModel):
    llcs: List[llcFullDTO]

class llcDelDTO(BaseModel):
    llc : str

class llcsListDTO(BaseModel):
    llcs: List[llcDTO]

class llcsDelListDTO(BaseModel):
    llcs: List[llcDelDTO]