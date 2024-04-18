from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint, UniqueConstraint
from ..database.db import Base
from sqlalchemy.orm import relationship
from property_master_model import PropertyMaster

class BusinessRulesLogic(Base):
    __tablename__ = "business_rules_logic"

    id = Column(Integer, primary_key=True, index=True)
    key1 = Column(String,nullable=False,index=True)
    op1 = Column(String,nullable=False,index=True)
    val1 = Column(String,nullable=False,index=True)
    key2 = Column(String,nullable=False,index=True)
    op2 = Column(String,nullable=False,index=True)
    val2 = Column(String,nullable=False,index=True)
    key3 = Column(String,nullable=False,index=True)
    op3 = Column(String,nullable=False,index=True)
    val3 = Column(String,nullable=False,index=True)
    key4 = Column(String,nullable=False,index=True)
    op4 = Column(String,nullable=False,index=True)
    val4 = Column(String,nullable=False,index=True)
    transaction_group = Column(String)
    transaction_type = Column(String)
    vendor = Column(String)
    customer = Column(String)
    vendor_w9 = Column(String)
    customer_w9 = Column(String)
    __table_args__ = (
        UniqueConstraint('key1', 'op1','val1','key2','op2','val2','key3','op3','val3','key4','op4','val4', name='uix_business_rules_logic'),
    )