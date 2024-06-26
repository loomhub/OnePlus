import logging
from typing import List, Optional, Type
from fastapi import HTTPException
from pydantic import BaseModel

from ..models.bankaccounts_model import bankaccountsModel
from ..models.transaction_types_model import transactionTypesModel
from ..models.partners_model import partnersModel
from ..repositories.transaction_repository import transactionRepository
from .myservice import MyService

class transactionService(MyService):
    def __init__(self, transaction_repository: transactionRepository):
        super().__init__(transaction_repository)

    async def post_data(self, 
                        records:List[Type[BaseModel]], 
                        model: Type[BaseModel], 
                        update_flag:str,myObjects:str):
        
        results=[]
        errors=[]

        # Validate data
        fkey_checks = {bankaccountsModel: {'bank_account_key': 'bank_account_key'},
                       transactionTypesModel: {'transaction_group': 'transaction_group',
                                               'transaction_type': 'transaction_type'},
                        partnersModel: {'vendor':'partner'},
                        partnersModel: {'customer':'partner'}
                        }  # Fkey Model: {input data column: Model column}} 
        errors = await self.validate_data(records, fkey_checks)

        # Post data if no errors
        if not errors:
            for record in records:
                try:
                    key_fields = {'bank_account_key': record.bank_account_key,
                                    'tdate': record.tdate,
                                    'description': record.description,
                                    'amount': record.amount}  # Adjust according to actual key fields
                    created, result = await self.upsert_records(record, model, key_fields, update = update_flag)
                    results.append( {"created": created, myObjects: result} )
                except Exception as e:
                    logging.error(f"Failed to update or create record: {str(e)}")
                    raise HTTPException(status_code=400, detail=str(e))
        
        return results, errors