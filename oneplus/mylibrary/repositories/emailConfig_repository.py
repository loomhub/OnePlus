from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .myrepository import myRepository
from ..models.emailConfig_model import emailsConfigModel as myModel

class emailConfigRepository(myRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)