import logging
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Type
from ..models.llcs_model import llcsModel

from ..repositories.property_master_repository import propertyMasterRepository
from .myservice import MyService

class propertyMasterService(MyService):
    def __init__(self, propertyMaster_repository: propertyMasterRepository):
        super().__init__(propertyMaster_repository)
    
    async def post_data(self, 
                        records:List[Type[BaseModel]], 
                        model: Type[BaseModel], 
                        update_flag:str,myObjects:str):
        
        results=errors=[]

        # Validate data
        fkey_checks = {llcsModel: {'llc': 'llc'}}  # Fkey Model: {input data column: Model column}} 
        errors = await self.validate_data(records, fkey_checks)

        # Post data if no errors
        if not errors:
            for record in records:
                try:
                    key_fields = {'property_name': record.property_name}  # Adjust according to actual key fields
                    created, result = await self.upsert_records(record, model, key_fields, update = update_flag)
                    results.append( {"created": created, myObjects: result} )
                except Exception as e:
                    logging.error(f"Failed to update or create record: {str(e)}")
                    raise HTTPException(status_code=400, detail=str(e))
        
        return results, errors
   
