from sqlalchemy.ext.asyncio import AsyncSession
from .myrepository import myRepository


class BirdRepository(myRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)

class oneplus_mailRepository(myRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)
    
        
