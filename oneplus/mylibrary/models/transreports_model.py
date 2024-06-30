from sqlalchemy import Column, Integer, String, UniqueConstraint
from ..database.db import Base

class transreportModel(Base):
    __tablename__ = "transreports"

    id = Column(Integer, primary_key=True, index=True)
    sequence_id = Column(Integer, index=True, nullable=False)
    category = Column(String)
    calc_method = Column(String) 
    fields = Column(String)
    __table_args__ = (
        UniqueConstraint('sequence_id', name='uix_sequence_id'),
    )
