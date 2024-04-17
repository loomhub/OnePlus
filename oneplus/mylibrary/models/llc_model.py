from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint
from ..database.db import Base
from sqlalchemy.orm import relationship

class LLCMaster(Base):
    __tablename__ = "llc_master"

    id = Column(Integer, primary_key=True, index=True)
    llc = Column(String, index=True, nullable=False,unique = True)
    ein = Column(String)
    llc_address = Column(String) 
    __table_args__ = (
        UniqueConstraint('llc', name='uix_llc'),
    )
    