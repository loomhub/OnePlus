from pydantic import BaseModel

class llcDTO(BaseModel):
    llc : str
    ein : str
    llc_address : str 