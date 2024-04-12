from sqlalchemy import Column, Integer, String, Date, Numeric
from ..database.db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    description = Column(String)
    details = Column(String)
    amount = Column(Numeric(10, 2))
    classification = Column(String)
    asset = Column(String)
    transaction_group = Column(String)
    transaction_type = Column(String)
    vendor = Column(String)
    customer = Column(String)
    comments = Column(String)
