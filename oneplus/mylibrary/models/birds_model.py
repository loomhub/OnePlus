from sqlalchemy import Column, Integer, String, UniqueConstraint
from ..database.db import Base

class birdsModel(Base):
    __tablename__ = "bird"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True, nullable=False,unique = True)
    pwd = Column(String)
    active = Column(String)
    server = Column(String)
    port = Column(Integer)
    __table_args__ = (
        UniqueConstraint('sender', name='uix_sender'),
    )

