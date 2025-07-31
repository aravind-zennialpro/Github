from pydantic import BaseModel

class BookingRequest(BaseModel):
    passenger_name: str
    phone: str
    route_id: str
