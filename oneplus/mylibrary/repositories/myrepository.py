from datetime import date
from typing import Dict, List, Optional, Type
import pandas as pd
from pydantic import BaseModel
from sqlalchemy import extract, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

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
############################################################################################################
        
    async def retrieve_unique_record(self, model: Type[BaseModel], filters: dict,**kwargs) -> Optional[BaseModel]:
        """
       # Retrieve a unique record by multiple field filters.
       # :param model: SQLAlchemy model class
       # :param filters: Dictionary of field names and values to filter by
        """
        multiple = kwargs.get('multiple', None) 

        try:
            async with self.db_session as session:
                stmt = select(model)
                for field, value in filters.items():
                    if value:
                        stmt = stmt.where(getattr(model, field) == value)
                result = await session.execute(stmt)
                if multiple:
                    return result.scalars().all()
                return result.scalars().first()
        except SQLAlchemyError as e:
        # Handle specific database query errors
            await session.rollback()
            print(f"Database error during record retrieval: {e}")
            return None
        except Exception as e:
        # Handle any other exceptions that may not be related to the database
            print(f"An error occurred: {e}")
            return None
############################################################################################################            
    async def add_data(self, data_model: Type[BaseModel])-> BaseModel:
        try:
            self.db_session.add(data_model)
            await self.db_session.commit()
            return data_model
        except Exception as e:
            await self.db_session.rollback()
            raise e
#############################################################################################################    
    async def delete_data(self, data_model: Type[BaseModel]) -> bool:
        try:    
            async with self.db_session as session:
                await session.delete(data_model)
                await session.commit()
                return True
        except Exception as e:
            await self.db_session.rollback()
            raise e
############################################################################################################
    async def truncate_table(self, data_model: Type[BaseModel]) -> bool:
        try:    
            async with self.db_session as session:
                truncate_stmt = text(f'TRUNCATE TABLE {data_model.__tablename__} RESTART IDENTITY CASCADE;')
                await session.execute(truncate_stmt)
                await session.commit()
                return True
        except Exception as e:
            print(f"Error while truncating table {data_model.__tablename__}: {e}")
            await self.db_session.rollback()
            raise e
############################################################################################################
    async def commit_changes(self) -> None:
        try:
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise e
############################################################################################################
    async def rollback_changes(self) -> None:
        await self.db_session.rollback()
############################################################################################################
    # async def retrieve_summary_by_month(self, model, key, years, 
    #                                     keys: Dict[str, str], labels: Dict[str, str], 
    #                                     filter_values: List[str]):
    #     # Set years
    #     if not years:
    #         years = 2
    #     end_year = date.today().year
    #     start_year = end_year - years
        
    #     try:
    #         async with self.db_session as session:

    #             conditions = [
    #                 getattr(model, keys['filter_column']).in_(filter_values),
    #                 extract('year', getattr(model, keys['date'])).between(start_year, end_year)
    #             ]
                
    #             if key is not None:
    #                 conditions.append(getattr(model, keys['key']) == key)
                
    #             stmt = (
    #                 select(
    #                 getattr(model, keys['key']),
    #                 extract('year', getattr(model, keys['date'])).label('year'),
    #                 extract('month', getattr(model, keys['date'])).label('month'),
    #                 func.sum(getattr(model, labels['amount'])).label(labels['amount'])
    #         )
    #         .where(*conditions)
    #         .group_by(
    #                     getattr(model, keys['key']),
    #                     extract('year', getattr(model, keys['date'])),
    #                     extract('month', getattr(model, keys['date']))
    #                 )
    #                 .order_by(
    #                     getattr(model, keys['key']),
    #                     extract('year', getattr(model, keys['date'])),
    #                     extract('month', getattr(model, keys['date']))
    #                 )
    #         )
    #             result = await session.execute(stmt)
    #             return result.fetchall()

    #     except SQLAlchemyError as e:
    #         # Handle specific database query errors
    #             await session.rollback()
    #             print(f"Database error during record retrieval: {e}")
    #             return None
    #     except Exception as e:
    #         # Handle any other exceptions that may not be related to the database
    #             print(f"An error occurred: {e}")
    #             return None
