from sqlalchemy import Column, Integer, String
from db.mysql import Base

class MySQLItem(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String(255))
