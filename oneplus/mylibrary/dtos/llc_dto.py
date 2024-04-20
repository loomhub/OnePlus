from datetime import date
from pydantic import BaseModel

class llcDTO(BaseModel):
    llc : str
    ein : str
    llc_address : str 
    llc_description : str
    formation_date : date