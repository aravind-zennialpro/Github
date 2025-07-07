# schemas.py

from pydantic import BaseModel
from datetime import datetime

class RouteCreate(BaseModel):
    source: str
    destination: str
    fare: float
    departure_time: str

class RouteOut(RouteCreate):
    id: int
    class Config:
        orm_mode = True

class BookingCreate(BaseModel):
    passenger_name: str
    phone: str
    route_id: int

class BookingOut(BaseModel):
    id: int
    passenger_name: str
    phone: str
    route: RouteOut
    timestamp: datetime

class RouteUpdate(BaseModel):
    source: str | None = None
    destination: str | None = None
    fare: float | None = None
    departure_time: str | None = None
    
    class Config:
        from_attributes = True
