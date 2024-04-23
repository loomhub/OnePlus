from typing import List
from pydantic import BaseModel


class birdDTO(BaseModel):
    sender : str
    pwd : str
    class Config:
        orm_mode = True

class oneplus_mail_DTO(BaseModel):
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