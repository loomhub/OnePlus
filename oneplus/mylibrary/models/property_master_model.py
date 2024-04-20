from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint,ForeignKey
from ..database.db import Base
from sqlalchemy.orm import relationship
#from ..models.llc_model import Llcs

class PropertyMaster(Base):
    __tablename__ = "property_master"

    id = Column(Integer, primary_key=True, index=True)
    property_name = Column(String,unique=True, index=True, nullable=False)
    property_description = Column(String)
    llc = Column(String,ForeignKey('llcs.llc')) 
    note = Column(String,CheckConstraint('note IN ("LLC","VJ","NG","PG")'))
    account_type = Column(String,CheckConstraint('account_type IN ("Checking","Savings")'))
    bank_name = Column(String)
    account_number = Column(Numeric(10, 0))
    __table_args__ = (
        UniqueConstraint('property_name', name='uix_property_name'),
    )
    llc_entity = relationship("Llcs")