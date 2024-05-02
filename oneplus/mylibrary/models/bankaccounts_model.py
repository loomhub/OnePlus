from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint,ForeignKey
from ..database.db import Base

class bankaccountsModel(Base):
    __tablename__ = "bankaccounts"

    id = Column(Integer, primary_key=True, index=True)
    bank_account_key = Column(String, index=True, nullable=False)
    bank = Column(String, index=True, nullable=False)
    account_type = Column(String, index=True, nullable=False)
    account_number = Column(String, index=True, nullable=False)
    llc = Column(String, ForeignKey('llcs.llc'), index=True, nullable=False)
    property_name = Column(String, ForeignKey('property_master.property_name'), index=True, nullable=True)
    __table_args__ = (
        UniqueConstraint('bank_account_key', name='uix_bankaccountkey'),
    )
