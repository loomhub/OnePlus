import logging
from typing import List, Type
from fastapi import HTTPException
from pydantic import BaseModel

from ..models.llcs_model import llcsModel
from ..models.property_master_model import propertyMastersModel
from ..repositories.sample_repository import sampleRepository
from .myservice import MyService


class sampleService(MyService):
    def __init__(self, sample_repository: sampleRepository):
        super().__init__(sample_repository)

    async def post_data(self, 
                        records:List[Type[BaseModel]], 
                        model: Type[BaseModel], 
                        update_flag:str,myObjects:str):
        
        results=[]
        errors=[]

        # Validate data
        fkey_checks = {llcsModel: {'llc': 'llc'}, propertyMastersModel: {'property_name':'property_name'}}  # Fkey Model: {input data column: Model column}} 
        errors = await self.validate_data(records, fkey_checks)

        # Post data if no errors
        if not errors:
            for record in records:
                try:
                    key_fields = {'sample': record.sample}  # Adjust according to actual key fields
                    created, result = await self.upsert_records(record, model, key_fields, update = update_flag)
                    results.append( {"created": created, myObjects: result} )
                except Exception as e:
                    logging.error(f"Failed to update or create record: {str(e)}")
                    raise HTTPException(status_code=400, detail=str(e))
        
        return results, errors
   
