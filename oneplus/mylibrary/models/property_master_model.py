from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint
from ..database.db import Base
from sqlalchemy.orm import relationship

class PropertyMaster(Base):
    __tablename__ = "property_master"

    id = Column(Integer, primary_key=True, index=True)
    property_name = Column(String,primary_key=True, index=True)
    property_description = Column(String)
    LLC = Column(String) 
    note = Column(String,CheckConstraint('note IN ("LLC","VJ","NG","PG")'))
    account_type = Column(String,CheckConstraint('account_type IN ("Checking","Savings")'))
    bank_name = Column(String)
    account_number = Column(Numeric(10, 0))