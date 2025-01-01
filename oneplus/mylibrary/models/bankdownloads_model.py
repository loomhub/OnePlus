from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint,ForeignKey,Text
from ..database.db import Base

class bankdownloadsModel(Base):
    __tablename__ = "bankdownloads"

    id = Column(Integer, primary_key=True, index=True)
    bank_account_key = Column(String,ForeignKey('bankaccounts.bank_account_key'),nullable=False,index=True)
    tdate = Column(Date,nullable=False,index=True)
    description = Column(Text,nullable=False, index=True)
    amount = Column(Numeric(10, 2),nullable=False,index=True)
    __table_args__ = (
        UniqueConstraint('bank_account_key','tdate', 'description','amount', name='uix_bankdownloads'),
    )
    