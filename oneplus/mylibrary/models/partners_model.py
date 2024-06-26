from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint
from ..database.db import Base
from sqlalchemy.orm import relationship

class partnersModel(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    partner = Column(String, index=True, nullable=False,unique = True)
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
        UniqueConstraint('partner', name='uix_partner'),
    )
    