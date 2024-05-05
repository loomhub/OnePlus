import logging
from typing import List, Type
from fastapi import HTTPException
from pydantic import BaseModel

from ..repositories.llc_repository import LLCRepository
from .myservice import MyService

class llcService(MyService):
    def __init__(self, llc_repository: LLCRepository):
        super().__init__(llc_repository)

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
                    key_fields = {'llc': record.llc}  # Adjust according to actual key fields
                    created, result = await self.upsert_records(record, model, key_fields, update = update_flag)
                    results.append( {"created": created, myObjects: result} )
                except Exception as e:
                    logging.error(f"Failed to update or create record: {str(e)}")
                    raise HTTPException(status_code=400, detail=str(e))
        
        return results, errors
   

