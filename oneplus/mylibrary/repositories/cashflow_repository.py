from sqlalchemy.ext.asyncio import AsyncSession
from .myrepository import myRepository

class cashflowRepository(myRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)

