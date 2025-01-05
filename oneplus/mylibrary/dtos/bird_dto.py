from typing import List, Optional
from pydantic import BaseModel, Field


class birdDTO(BaseModel):
    sender : Optional[str] = None
    pwd : Optional[str] = None
    active : Optional[str] = None
    server : Optional[str] = None
    port : Optional[int] = None
    class Config:
        from_attributes = True

class birdDelDTO(BaseModel):
    sender : Optional[str] = None

class birdsDelListDTO(BaseModel):
    birdsDel: List[birdDelDTO]

class birdsListDTO(BaseModel):
    birds: List[birdDTO]

class birdQueryPrimaryKey(BaseModel):
    sender: str = Field(None, description="Name of the bird to filter by")

class birdQueryUpdateFlag(BaseModel):
    update: Optional[str] = Field(None, description="Set X to update the record even if it exists")
