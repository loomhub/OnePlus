import logging
from typing import List, Type
from fastapi import HTTPException
from pydantic import BaseModel

from ..models.llcs_model import llcsModel
from ..models.property_master_model import propertyMastersModel
from ..repositories.transaction_type_repository import transactionTypeRepository
from .myservice import MyService

# class transactionTypesModel(Base):
#     __tablename__ = "transaction_types"

#     id = Column(Integer, primary_key=True, index=True)
#     transaction_group = Column(String, index=True, nullable=False)
#     transaction_type = Column(String, index=True, nullable=False)
#     transaction_description = Column(String)
#     # Define the composite unique constraint
#     __table_args__ = (
#         UniqueConstraint('transaction_type', 'transaction_group', 
#                          name='uix_transaction_type_group'),
#     )

class transactionTypeService(MyService):
    def __init__(self, transactionType_repository: transactionTypeRepository):
        super().__init__(transactionType_repository)

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
                    key_fields = {'transaction_type': record.transaction_type,
                                    'transaction_group': record.transaction_group}  # Adjust according to actual key fields
                    created, result = await self.upsert_records(record, model, key_fields, update = update_flag)
                    results.append( {"created": created, myObjects: result} )
                except Exception as e:
                    logging.error(f"Failed to update or create record: {str(e)}")
                    raise HTTPException(status_code=400, detail=str(e))
        
        return results, errors
   
