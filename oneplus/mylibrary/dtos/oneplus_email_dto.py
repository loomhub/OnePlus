from typing import List
from pydantic import BaseModel


class birdDTO(BaseModel):
    sender : str
    pwd : str
    class Config:
        orm_mode = True

class oneplusMailDTO(BaseModel):
    subject : str
    receiver : str
    cc : str
    bcc : str
    class Config:
        orm_mode = True

class birdDelDTO(BaseModel):
    sender : str

class birdsDelListDTO(BaseModel):
    birds: List[birdDelDTO]

class birdListDTO(BaseModel):
    birds: List[birdDTO]

class oneplusMailListDTO(BaseModel):
    oneplusMails: List[oneplusMailDTO]