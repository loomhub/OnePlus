from typing import Type, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from .myrepository import myRepository

class ruleRepository(myRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)
