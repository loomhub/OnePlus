from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint,ForeignKey,Text
from ..database.db import Base

class transactionstmpModel(Base):
    __tablename__ = "transactionstmp"

    id = Column(Integer, primary_key=True, index=True)
    bank_account_key = Column(String,nullable=False,index=True)
    tdate = Column(Date,nullable=False,index=True)
    description = Column(Text,nullable=False, index=True)
    amount = Column(Numeric(10, 2),nullable=False,index=True)
    classification = Column(String)
    period_status = Column(String)
    transaction_group = Column(String)
    transaction_type = Column(String)
    vendor = Column(String)
    customer = Column(String)
    comments = Column(String)
    vendor_no_w9 = Column(String)
    customer_no_w9 = Column(String)
    __table_args__ = (
        UniqueConstraint('bank_account_key','tdate', 'description','amount', name='uix_transactionstmp'),
    )
