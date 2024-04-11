from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from typing import Generator

# Environment variables for database connection or hardcoded values
#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost/oneplusdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()