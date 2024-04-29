from sqlalchemy import Column, Integer, String, UniqueConstraint
from ..database.db import Base

class emailsConfigModel(Base):
    __tablename__ = "emails_config"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True, nullable=False,unique = True)
    endpoint = Column(String,index=True, nullable=False,unique = True)
    to = Column(String,index=True, nullable=False,unique = True) 
    cc = Column(String)  
    bcc = Column(String) 
    inactive = Column(String,nullable=False,unique = True)  
    
