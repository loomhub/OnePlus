from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint
from ..database.db import Base
from sqlalchemy.orm import relationship

class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer = Column(String, index=True, nullable=False,unique = True)
    recipient_type = Column(String,CheckConstraint('recipient_type IN ("Individual","Business")'))
    recipient_tin_type = Column(String,CheckConstraint('recipient_tin_type IN ("SSN","EIN")'))
    recipient_tin = Column(String)
    last_name = Column(String)
    first_name = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String)
    __table_args__ = (
        UniqueConstraint('customer', name='uix_customer'),
    )
    