# app/routes/search_routes.py
from fastapi import APIRouter, HTTPException
from app.models import SearchRequest, SearchResponse, WeatherInfo, BusInfo, HotelInfo, BookingRequest, BookingResponse
from app.services.weather_service import get_weather_summary_for_city
from app.services.hotel_service import search_hotels, get_hotel_by_id
from app.services.bus_service import search_buses, get_bus_by_id
from app.db import bookings_collection
import uuid
from datetime import datetime
from typing import List

router = APIRouter()

def make_suggestion_from_weather(weather_summary: str, user_name: str = "Traveler"):
    s = weather_summary.lower()
    if "rain" in s or "heavy" in s:
        return f"Hey {user_name}, it's expected to be {weather_summary} — consider postponing your trip if possible."
    if "fog" in s or "mist" in s:
        return f"Hey {user_name}, visibility may be low ({weather_summary}). Travel carefully; allow extra time."
    if "cloud" in s:
        return f"Hi {user_name}, weather is {weather_summary}. Trip looks okay but carry a light jacket."
    return f"Great news {user_name}! Weather looks {weather_summary}. Have a safe journey!"

@router.post("/search", response_model=SearchResponse)
async def search_travel(req: SearchRequest):
    # 1. Weather at destination
    weather = await get_weather_summary_for_city(req.to_city, req.depart_date)
    weather_info = WeatherInfo(summary=weather["summary"], temp_c=weather.get("temp_c"), precipitation=weather.get("precipitation"))

    # 2. Buses (mocked, with IDs)
    buses_raw = await search_buses(req.from_city, req.to_city, req.depart_date)
    buses = [BusInfo(**b) for b in buses_raw]

    # 3. Hotels (with IDs)
    hotels_raw = await search_hotels(req.to_city, limit=5)
    hotels = [HotelInfo(**h) for h in hotels_raw]

    # 4. suggestion
    suggestion = make_suggestion_from_weather(weather_info.summary)

    return SearchResponse(weather=weather_info, buses=buses, hotels=hotels, suggestion=suggestion)

@router.post("/book", response_model=BookingResponse)
async def create_booking(b: BookingRequest):
    
    # Book a trip using bus_id and hotel_id, but save full details into MongoDB.
    
    # 1. searching bus details
    bus = await get_bus_by_id(b.bus_id, b.from_city, b.to_city, b.depart_date)
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    # 2. searching hotel details
    hotel = await get_hotel_by_id(b.hotel_id, b.to_city)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    # 3. Prepare booking document
    booking_id = str(uuid.uuid4())
    doc = {
        "user_name": b.user_name,
        "email": b.email,
        "from_city": b.from_city,
        "to_city": b.to_city,
        "depart_date": b.depart_date,
        "bus": bus,        #  full bus info
        "hotel": hotel,    #  full hotel info
        "booking_id": booking_id,
        "created_at": datetime.utcnow().isoformat()
    }

    # 4. Save in MongoDB
    await bookings_collection.insert_one(doc)

    return BookingResponse(booking_id=booking_id, message="Booking saved. Have a safe trip!")

@router.get("/bookings")
async def get_all_bookings():

    # Get all saved bookings from MongoDB with full bus & hotel info.

    bookings_cursor = bookings_collection.find({})
    bookings = []
    async for doc in bookings_cursor:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        bookings.append(doc)
    return {"count": len(bookings), "bookings": bookings}
