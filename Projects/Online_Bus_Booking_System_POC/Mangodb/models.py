from beanie import Document
from pydantic import BaseModel, Field

class Route(Document):
    id: int = Field(..., alias="_id")  # Use integer as MongoDB _id
    source: str
    destination: str
    fare: int

    class Settings:
        name = "routes"  # MongoDB collection name

class Booking(Document):
    passenger_name: str
    phone: str
    route_id: str
    timestamp: str

    class Settings:
        name = "bookings"
