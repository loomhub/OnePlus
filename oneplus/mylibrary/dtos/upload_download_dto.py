from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional

class fileDTO(BaseModel):
    Property : Optional[str] = None
    Month : Optional[date] = None
    Balance : Optional[float] = None
    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d'),
            float: lambda v: float('nan') if v in [float('inf'), float('-inf'), float('nan')] else v
        }


class fileListDTO(BaseModel):
    objects: List[fileDTO]


