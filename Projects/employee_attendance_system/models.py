from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, index=True)
    action = Column(String)  # "checkin" or "checkout"
    timestamp = Column(DateTime, default=datetime.utcnow)
