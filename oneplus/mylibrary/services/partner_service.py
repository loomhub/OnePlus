import logging
from typing import List, Type
from fastapi import HTTPException
from pydantic import BaseModel

from ..models.llcs_model import llcsModel
from ..models.property_master_model import propertyMastersModel
from ..repositories.partner_repository import partnerRepository
from .myservice import MyService
    
class partnerService(MyService):
    def __init__(self, partner_repository: partnerRepository):
        super().__init__(partner_repository)

    async def post_data(self, 
                        records:List[Type[BaseModel]], 
                        model: Type[BaseModel], 
                        update_flag:str,myObjects:str):
        
        results=[]
        errors=[]

        # Validate data
        validate_key= {'receipient_type': ('Individual','Business'), 'recipient_tin_type': ('SSN','EIN')}
        errors = await self.validate_value_contraints(records, validate_key)

        # Post data if no errors
        if not errors:
            for record in records:
                try:
                    key_fields = {'partner': record.partner}  # Adjust according to actual key fields
                    created, result = await self.upsert_records(record, model, key_fields, update = update_flag)
                    results.append( {"created": created, myObjects: result} )
                except Exception as e:
                    logging.error(f"Failed to update or create record: {str(e)}")
                    raise HTTPException(status_code=400, detail=str(e))
        
        return results, errors
   
