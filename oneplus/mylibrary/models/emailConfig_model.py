from sqlalchemy import Column, Integer, String, UniqueConstraint
from ..database.db import Base

class emailsConfigModel(Base):
    __tablename__ = "emails_config"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True, nullable=False,unique = True)
    endpoint = Column(String)
    to = Column(String) 
    cc = Column(String)  
    bcc = Column(String) 
    inactive = Column(String)  
    __table_args__ = (
        UniqueConstraint('subject', name='uix_subject'),
    )
