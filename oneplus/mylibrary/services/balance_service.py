import logging
from typing import List, Type
from fastapi import HTTPException
from pydantic import BaseModel
from ..models.bankaccounts_model import bankaccountsModel
from ..repositories.balance_repository import balanceRepository
from .myservice import MyService

class balanceService(MyService):
    def __init__(self, balance_repository: balanceRepository):
        super().__init__(balance_repository)
   
    async def post_data(self, 
                        records:List[Type[BaseModel]], 
                        model: Type[BaseModel], 
                        update_flag:str,myObjects:str):
        
        results=[]
        errors=[]

        # Validate data
        fkey_checks = {bankaccountsModel: {'bank_account_key': 'bank_account_key'}}  # Fkey Model: {input data column: Model column}} 
        errors = await self.validate_data(records, fkey_checks)

        # Post data if no errors
        if not errors:
            for record in records:
                try:
                    key_fields = {'bank_account_key': record.bank_account_key,
                                'snapshot': record.snapshot}  # Adjust according to actual key fields
                    created, result = await self.upsert_records(record, model, key_fields, update = update_flag)
                    results.append( {"created": created, myObjects: result} )
                except Exception as e:
                    logging.error(f"Failed to update or create record: {str(e)}")
                    raise HTTPException(status_code=400, detail=str(e))
        
        return results, errors
   
