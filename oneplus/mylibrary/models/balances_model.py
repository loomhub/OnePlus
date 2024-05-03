from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint,ForeignKey
from ..database.db import Base

class balancesModel(Base):
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True, index=True)
    bank_account_key = Column(String,ForeignKey('bankaccounts.bank_account_key'), index=True, nullable=False)
    snapshot = Column(Date, index=True, nullable=False)
    balance = Column(Numeric(10, 2))
    __table_args__ = (
        UniqueConstraint('bank_account_key','snapshot', name='uix_balancekey_snapshot'),
    )
