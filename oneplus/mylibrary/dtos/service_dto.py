from typing import List, Optional
from pydantic import BaseModel, Field


class processedDTO(BaseModel):
    report : Optional[str] = None
    receiver : Optional[str] = None

class listProcessedDTO(BaseModel):
    done: List[processedDTO] = []

class QueryEmail(BaseModel):
    receiver: Optional[str] = Field(None, description="Name of the email receiver")
    keyword: Optional[str] = Field(None, description="Search keyword")