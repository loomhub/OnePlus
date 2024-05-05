import logging
from typing import List, Type
from fastapi import HTTPException
from pydantic import BaseModel
from ..models.emailConfig_model import emailsConfigModel
from ..repositories.emailConfig_repository import emailConfigRepository
from ..dtos.emailConfig_dto import emailsConfigListDTO
from .myservice import MyService

class emailConfigService(MyService):
    def __init__(self, emailConfig_repository: emailConfigRepository):
        super().__init__(emailConfig_repository)
    
    async def post_data(self, 
                        records:List[Type[BaseModel]], 
                        model: Type[BaseModel], 
                        update_flag:str,myObjects:str):
        
        results=[]
        errors=[]
        # Post data if no errors
        if not errors:
            for record in records:
                try:
                    key_fields = {'subject': record.subject,
                                  'endpoint':record.endpoint,
                                  'to':record.to,
                                  'cc':record.cc,
                                  'bcc':record.bcc}  # Adjust according to actual key fields
                    created, result = await self.upsert_records(record, model, key_fields, update = update_flag)
                    results.append( {"created": created, myObjects: result} )
                except Exception as e:
                    logging.error(f"Failed to update or create record: {str(e)}")
                    raise HTTPException(status_code=400, detail=str(e))
        
        return results, errors
   

   
