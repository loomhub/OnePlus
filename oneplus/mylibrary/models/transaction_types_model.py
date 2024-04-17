from sqlalchemy import Column, Integer, String, Date, Numeric,CheckConstraint,UniqueConstraint
from ..database.db import Base
from sqlalchemy.orm import relationship
class LLCMaster(Base):
    __tablename__ = "transaction_types"

    id = Column(Integer, primary_key=True, index=True)
    transaction_group = Column(String, index=True, nullable=False)
    transaction_type = Column(String, index=True, nullable=False)
    transaction_description = Column(String)
    # Define the composite unique constraint
    __table_args__ = (
        UniqueConstraint('transaction_type', 'transaction_group', 
                         name='uix_transaction_type_group'),
    )