from typing import Optional, Tuple, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from ..repositories.myrepository import myRepository  # Assuming a base repository exists
# Define a type variable that can be any subclass of BaseModel
DTO = TypeVar('DTO', bound=BaseModel)


class MyService:
    def __init__(self, repository: myRepository):
        self.repository = repository

    ############################################################################################################    

    async def extract_all(self, model: Type[BaseModel]) -> Optional[list]:
        try:
            return await self.repository.retrieve_all(model)
        except Exception as e:
            await self.repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")

    ############################################################################################################
    async def extract_pkey(self,model: Type[BaseModel],pkey: dict) -> Optional[BaseModel]:
        try:
            result = await self.repository.retrieve_unique_record(model, pkey)
            if result is None:
                print("Record not found")
            return result
        except SQLAlchemyError as e:  # Handling more specific database errors
            await self.repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")
        # except Exception as e:  # General exception if needed, though specific ones are preferred
        #     await self.repository.rollback_changes()
        #     raise Exception(f"Unexpected error: {str(e)}")

    ############################################################################################################

    async def upsert_records(self, data_dto:DTO, model: Type[BaseModel], key_fields: dict) -> Tuple[bool, BaseModel]:
        """
        Upsert an entity based on the provided data.
        :param data_dto: Data transfer object containing entity details
        :param model: The SQLAlchemy model class of the entity
        :param key_fields: Dictionary of key fields and their corresponding values from data_dto
        :return: Tuple containing boolean (True if created, False if updated) and entity instance
        """
        try:
            filters = {field: getattr(data_dto, field) for field in key_fields}
            entity_instance = await self.repository.retrieve_unique_record(model, filters)

            if entity_instance:
                # Update it
                deleted = await self.repository.delete_data(entity_instance)
                await self.repository.commit_changes()
            
            entity_instance = model(**data_dto.dict())
            self.repository.db_session.add(entity_instance)
            await self.repository.db_session.commit()
            created = True
            return created, entity_instance

        except Exception as e:
            # Handle specific database errors or re-raise
            await self.repository.rollback_changes()
            raise Exception(f"Database error: {str(e)}")
############################################################################################################
    async def delete_records(self, data_dto:DTO, model: Type[BaseModel], key_fields: dict) -> Tuple[bool, BaseModel]:
           """
           Delete an entity based on the provided data.
            :param data_dto: Data transfer object containing entity details
            :param model: The SQLAlchemy model class of the entity
            :param key_fields: Dictionary of key fields and their corresponding values from data_dto
            :return: Tuple containing boolean and entity instance
           """
           try:
            filters = {field: getattr(data_dto, field) for field in key_fields}
            entity_instance = await self.repository.retrieve_unique_record(model, filters)

            if entity_instance:
                deleted = await self.repository.delete_data(entity_instance)
                await self.repository.commit_changes()
            else:
                   # LLC not found
                deleted = False

            await self.repository.commit_changes()
            return deleted,entity_instance

           except Exception as e:
               # Handle specific database errors or re-raise
               await self.repository.rollback_changes()
               raise Exception(f"Database error: {str(e)}")
