from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint,ForeignKey
from ..database.db import Base
from sqlalchemy.orm import relationship

class propertyMastersModel(Base):
    __tablename__ = "property_master"

    id = Column(Integer, primary_key=True, index=True)
    property_name = Column(String,unique=True, index=True, nullable=False)
    property_description = Column(String)
    llc = Column(String,ForeignKey('llcs.llc')) 
    note = Column(String,CheckConstraint('note IN ("LLC","VJ","NG","PG")'))
    purchase_date = Column(Date)
    sell_date = Column(Date)
    purchase_price = Column(Numeric(10, 2))
    sell_price = Column(Numeric(10, 2))
    units = Column(Integer)
    county = Column(String)
    __table_args__ = (
        UniqueConstraint('property_name', name='uix_property_name'),
    )
