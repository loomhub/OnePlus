from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint,ForeignKey
from ..database.db import Base

class transactionsModel(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    bank_account_key = Column(String,ForeignKey('bankaccounts.bank_account_key'),nullable=False,index=True)
    tdate = Column(Date,nullable=False,index=True)
    description = Column(String,nullable=False, index=True)
    amount = Column(Numeric(10, 2),nullable=False,index=True)
    classification = Column(String)
    period_status = Column(String)
    transaction_group = Column(String,ForeignKey('transaction_types.transaction_group'))
    transaction_type = Column(String,ForeignKey('transaction_types.transaction_type'))
    vendor = Column(String,ForeignKey('vendors.vendor'))
    customer = Column(String,ForeignKey('customers.customer'))
    comments = Column(String)
    vendor_no_w9 = Column(String)
    customer_no_w9 = Column(String)
    __table_args__ = (
        UniqueConstraint('bank_account_key','tdate', 'description','amount', name='uix_transaction'),
    )
    