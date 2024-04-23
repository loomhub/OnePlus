from sqlalchemy import Column, Integer, String,Date, UniqueConstraint
from ..database.db import Base

class Birds(Base):
    __tablename__ = "bird"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True, nullable=False,unique = True)
    pwd = Column(String)
    __table_args__ = (
        UniqueConstraint('sender', name='uix_sender'),
    )

class Oneplus_mails(Base):
    __tablename__ = "oneplus_mail"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True, nullable=False,unique = True)
    receiver = Column(String,nullable=False,unique = True)
    cc = Column(String,nullable=True,unique = True)
    bcc = Column(String,nullable=True,unique = True)
    __table_args__ = (
        UniqueConstraint('subject','receiver','cc','bcc', name='uix_mail'),
    )