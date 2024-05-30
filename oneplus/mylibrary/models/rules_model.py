from sqlalchemy import Column, Integer, String,UniqueConstraint
from ..database.db import Base

class rulesModel(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    ttype = Column(String,nullable=False,index=True)
    description = Column(String,nullable=True,index=True)
    transaction_group = Column(String)
    transaction_type = Column(String)
    vendor = Column(String)
    customer = Column(String)
    vendor_no_w9 = Column(String)
    customer_no_w9 = Column(String)
    __table_args__ = (
        UniqueConstraint('ttype','description', name='uix_rules'),
    )
