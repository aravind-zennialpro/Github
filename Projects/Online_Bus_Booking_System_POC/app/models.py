# models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    destination = Column(String)
    fare = Column(Float)
    departure_time = Column(String)

    bookings = relationship("Booking", back_populates="route")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    passenger_name = Column(String)
    phone = Column(String)
    route_id = Column(Integer, ForeignKey("routes.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    route = relationship("Route", back_populates="bookings")
