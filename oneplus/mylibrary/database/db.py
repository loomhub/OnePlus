from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from sqlalchemy import create_engine


# Environment variables for database connection or hardcoded values
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:54321/oneplusrealtydb"
SYNC_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:54321/oneplusrealtydb"

async_engine = create_async_engine(DATABASE_URL, echo=True)
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)

AsyncSessionFactory = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with AsyncSessionFactory() as session:
            yield session
    
    finally:
        await session.close()