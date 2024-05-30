from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint,ForeignKey
from ..database.db import Base

class cashflowsModel(Base):
    __tablename__ = "cashflows"

    id = Column(Integer, primary_key=True, index=True)
    bank_account_key = Column(String,ForeignKey('bankaccounts.bank_account_key'), index=True, nullable=False)
    start_date = Column(Date, index=True, nullable=False)
    end_date = Column(Date, index=True, nullable=False)
    cash_change = Column(Numeric(10, 2))
    ending_balance = Column(Numeric(10, 2))
    calc_balance = Column(Numeric(10, 2))
    period_status = Column(String, index=True, nullable=False)

    __table_args__ = (
        UniqueConstraint('bank_account_key','start_date','end_date', name='uix_cashflowkey_start_end'),
    )
