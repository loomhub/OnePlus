from typing import Type, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from .myrepository import myRepository

class transactiontmpRepository(myRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)

#result = await self.repository.retrieve_search_records(model, search_fields)
#return result
    async def retrieve_search_records(self, model: Type[BaseModel], filters: dict,**kwargs) -> Optional[list]:
       """
      # Retrieve a unique record by multiple field filters.
      # :param model: SQLAlchemy model class
      # :param filters: Dictionary of field names and values to filter by
       """
       try:
            async with self.db_session as session:
                stmt = select(model)
                for field, value in filters.items():
                    if value and field == "start_date":
                        stmt = stmt.where(model.tdate >= value)
                    elif value and field == "end_date":
                        stmt = stmt.where(model.tdate <= value)
                    elif value and field == "min_amount":
                        stmt = stmt.where(model.amount >= value)
                    elif value and field == "max_amount":
                        stmt = stmt.where(model.amount <= value)
                    elif value and field == "description":
                        stmt = stmt.where(model.description.ilike(f"%{value}%"))
                    elif value:
                        stmt = stmt.where(getattr(model, field) == value) 
                result = await session.execute(stmt)
                return result.scalars().all()
       except SQLAlchemyError as e:
       # Handle specific database query errors
            await session.rollback()
            print(f"Database error during record retrieval: {e}")
            return None
       except Exception as e:
       # Handle any other exceptions that may not be related to the database
            print(f"An error occurred: {e}")
            return None