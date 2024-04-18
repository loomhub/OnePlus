from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint
from ..database.db import Base
from sqlalchemy.orm import relationship

class Tenants(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    customer = Column(String, index=True, nullable=False,unique = True)
    property_name = Column(String, index=True, nullable=False)
    unit_name = Column(String)
    lease_start = Column(Date)
    lease_end = Column(Date)
    rent = Column(Numeric(10, 2))
    security_deposit = Column(Numeric(10, 2))
    __table_args__ = (
        UniqueConstraint('customer','property_name', name='uix_tenant'),
    )
    