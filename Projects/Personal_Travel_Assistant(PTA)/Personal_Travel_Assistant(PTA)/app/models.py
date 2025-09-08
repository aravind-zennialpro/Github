# app/models.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class SearchRequest(BaseModel):
    from_city: str
    to_city: str
    depart_date: Optional[str] = None

class BusInfo(BaseModel):
    id: int
    operator: str
    departure_time: str
    arrival_time: str
    duration: str
    price: float
    bus_type: Optional[str] = "AC"

class HotelInfo(BaseModel):
    id: int
    name: str
    address: Optional[str]
    price_per_night: Optional[float]
    rating: Optional[float]

class WeatherInfo(BaseModel):
    summary: str
    temp_c: Optional[float]
    precipitation: Optional[float]

class SearchResponse(BaseModel):
    weather: WeatherInfo
    buses: List[BusInfo]
    hotels: List[HotelInfo]
    suggestion: str

class BookingRequest(BaseModel):
    user_name: str
    email: Optional[str]
    from_city: str
    to_city: str
    depart_date: str
    bus_id: int       # select bus by serial number
    hotel_id: int     # select hotel by serial number

class BookingResponse(BaseModel):
    booking_id: str
    message: str
