from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint
from ..database.db import Base
from sqlalchemy.orm import relationship
from property_master_model import PropertyMaster

class Transactions(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date,nullable=False,index=True)
    description = Column(String,nullable=False, index=True)
    details = Column(String,nullable=False, index=True)
    amount = Column(Numeric(10, 2),nullable=False,index=True)
    classification = Column(String)
    property_name = Column(String,foreign_key='property_master.property_name')
    transaction_group = Column(String)
    transaction_type = Column(String)
    vendor = Column(String)
    customer = Column(String)
    comments = Column(String)
    __table_args__ = (
        UniqueConstraint('date', 'description','details' ,'amount', name='uix_transaction'),
    )
    # This sets up a bidirectional relationship in SQLAlchemy, making it
    # easier to access the associated objects from both sides.
    property_rel = relationship("PropertyMaster", back_populates="transactions")

PropertyMaster.transactions = relationship("Transaction", order_by=Transaction.date, back_populates="property_rel")   