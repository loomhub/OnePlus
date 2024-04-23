from datetime import date
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.llc_model import Llcs
from .myrepository import myRepository

class LLCRepository(myRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)
    
    async def retrieve_llcs_by_name_and_date(self, llc_name: Optional[str] = None, start_date: Optional[date] = None):
        async with self.db_session as session:
            stmt = select(Llcs)
            if llc_name:
                stmt = stmt.where(Llcs.llc == llc_name)
            if start_date:
                stmt = stmt.where(Llcs.formation_date >= start_date)
            result = await session.execute(stmt)
            return result.scalars().all()
