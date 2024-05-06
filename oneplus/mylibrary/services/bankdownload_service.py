import logging
from typing import List, Type
from fastapi import HTTPException
from pydantic import BaseModel

from ..models.bankaccounts_model import bankaccountsModel
from ..repositories.bankdownload_repository import bankdownloadRepository
from .myservice import MyService

# class bankdownloadsModel(Base):
#     __tablename__ = "bankdownloads"

#     id = Column(Integer, primary_key=True, index=True)
#     bank_account_key = Column(String,ForeignKey('bankaccounts.bank_account_key'),nullable=False,index=True)
#     tdate = Column(Date,nullable=False,index=True)
#     description = Column(String,nullable=False, index=True)
#     amount = Column(Numeric(10, 2),nullable=False,index=True)
#     __table_args__ = (
#         UniqueConstraint('bank_account_key','tdate', 'description','amount', name='uix_bankdownloads'),
#     )
    

class bankdownloadService(MyService):
    def __init__(self, bankdownload_repository: bankdownloadRepository):
        super().__init__(bankdownload_repository)
    
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
                                'tdate': record.tdate,
                                'description': record.description,
                                'amount': record.amount
                                  }  # Adjust according to actual key fields
                    created, result = await self.upsert_records(record, model, key_fields, update = update_flag)
                    results.append( {"created": created, myObjects: result} )
                except Exception as e:
                    logging.error(f"Failed to update or create record: {str(e)}")
                    raise HTTPException(status_code=400, detail=str(e))
        
        return results, errors
   
   
