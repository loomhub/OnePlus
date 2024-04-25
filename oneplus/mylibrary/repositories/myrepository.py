from datetime import date
from typing import List, Optional, Type
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class myRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def retrieve_all(self,data_model: Type[BaseModel]) -> List[BaseModel]:
        try:
            async with self.db_session as session:
                stmt = select(data_model)
                result = await session.execute(stmt)
                return result.scalars().all()
        except Exception as e:
            raise e
        
    async def retrieve_unique_record(self, model: Type[BaseModel], filters: dict) -> Optional[BaseModel]:
        """
       # Retrieve a unique record by multiple field filters.
       # :param model: SQLAlchemy model class
       # :param filters: Dictionary of field names and values to filter by
        """
        try:
            async with self.db_session as session:
                stmt = select(model)
                for field, value in filters.items():
                    stmt = stmt.where(getattr(model, field) == value)
                result = await session.execute(stmt)
                return result.scalars().first()
        except Exception as e:
            raise e
            
    async def add_data(self, data_model: Type[BaseModel])-> BaseModel:
        try:
            self.db_session.add(data_model)
            await self.db_session.commit()
            return data_model
        except Exception as e:
            await self.db_session.rollback()
            raise e
    
    async def delete_data(self, data_model: Type[BaseModel]) -> bool:
        try:    
            async with self.db_session as session:
                await session.delete(data_model)
                await session.commit()
                return True
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def commit_changes(self) -> None:
        try:
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def rollback_changes(self) -> None:
        await self.db_session.rollback()
