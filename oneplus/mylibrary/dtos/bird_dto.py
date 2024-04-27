from typing import List, Optional
from pydantic import BaseModel, Field


class birdDTO(BaseModel):
    sender : Optional[str] = None
    pwd : Optional[str] = None
    class Config:
        orm_mode = True

class birdDelDTO(BaseModel):
    sender : Optional[str] = None

class birdsDelListDTO(BaseModel):
    birdsDel: List[birdDelDTO]

class birdsListDTO(BaseModel):
    birds: List[birdDTO]

class birdQueryPrimaryKey(BaseModel):
    sender: str = Field(None, description="Name of the bird to filter by")