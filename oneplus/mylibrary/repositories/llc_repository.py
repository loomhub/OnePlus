from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from ..models.llc_model import Llcs

class LLCRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_llc_by_name(self, llc_name: str):
        async with self.db_session as session:
            stmt = select(Llcs).where(Llcs.llc == llc_name)
            result = await session.execute(stmt)
            return result.scalars().first()
        
    async def get_llc_instances(self):
        async with self.db_session as session:
            stmt = select(Llcs)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def add_llc(self, llc_instance: Llcs):
        try:
            self.db_session.add(llc_instance)
            await self.db_session.commit()
            return llc_instance
        except Exception as e:
            await self.db_session.rollback()
            raise e
    
    async def delete_llc(self, llc_instance: Llcs):
        async with self.db_session as session:
            await session.delete(llc_instance)
            await session.commit()
            return llc_instance

    async def commit_changes(self):
        try:
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            raise e
        #await self.db_session.commit()

    async def rollback_changes(self):
        await self.db_session.rollback()
