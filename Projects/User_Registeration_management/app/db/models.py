from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserSQL(Base):
    __tablename__ = "users"

    username = Column(String(100), primary_key=True, unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    dob = Column(DateTime)
    doj = Column(DateTime)
    address = Column(String(255))
    comment = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
