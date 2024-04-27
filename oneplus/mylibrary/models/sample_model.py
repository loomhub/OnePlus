from sqlalchemy import Column, Integer, String,Date, UniqueConstraint
from ..database.db import Base

class samplesModel(Base):
    __tablename__ = "samples"

    id = Column(Integer, primary_key=True, index=True)
    llc = Column(String, index=True, nullable=False,unique = True)
    ein = Column(String)
    llc_address = Column(String) 
    llc_description = Column(String)  # New column for LLC description
    formation_date = Column(Date)  # New column for formation date
    __table_args__ = (
        UniqueConstraint('llc', name='uix_llc'),
    )
