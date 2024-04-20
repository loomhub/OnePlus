from sqlalchemy import Column, Integer, String,Date, UniqueConstraint
from ..database.db import Base
from sqlalchemy.orm import relationship
#from ..models.property_master_model import PropertyMaster

class Llcs(Base):
    __tablename__ = "llcs"

    id = Column(Integer, primary_key=True, index=True)
    llc = Column(String, index=True, nullable=False,unique = True)
    ein = Column(String)
    llc_address = Column(String) 
    __table_args__ = (
        UniqueConstraint('llc', name='uix_llc'),
    )
    # Establish relationship to PropertyMaster
  #  properties = relationship("PropertyMaster", back_populates="llc_entity")