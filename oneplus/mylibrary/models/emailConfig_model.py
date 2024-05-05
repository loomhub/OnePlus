from sqlalchemy import Column, Integer, String, UniqueConstraint
from ..database.db import Base

class emailsConfigModel(Base):
    __tablename__ = "emails_config"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True, nullable=False)
    endpoint = Column(String,index=True, nullable=False)
    to = Column(String,index=True, nullable=False) 
    cc = Column(String)  
    bcc = Column(String) 
    active = Column(String,nullable=False)  
    # Define the composite unique constraint
    __table_args__ = (
        UniqueConstraint('subject', 'endpoint', 'to', 'cc', 'bcc',
                         name='uix_email_config_subject_endpoint'),
    )
    
