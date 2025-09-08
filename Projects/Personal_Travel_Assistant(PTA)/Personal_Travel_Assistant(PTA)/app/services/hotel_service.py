# app/services/hotel_service.py
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
HOTEL_API_URL = os.getenv("HOTEL_API_URL", "https://api.makcorps.com/free")

async def search_hotels(city: str, limit: int = 5):
 # if api fails
    hotels = []
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(HOTEL_API_URL, params={"city": city})
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list) and len(data) > 0:
                    for i, h in enumerate(data[:limit]):
                        hotels.append({
                            "id": i + 1,  # serial number
                            "name": h.get("name", f"{city} Hotel {i+1}"),
                            "address": h.get("address", f"{city} center"),
                            "price_per_night": h.get("price", 2000),
                            "rating": h.get("rating", 4.0)
                        })
                    return hotels
    except Exception:
        pass

    # get back to mocked hotels (5 options)
    return [
        {"id": 1, "name": f"{city} Grand Hotel", "address": f"Central {city}", "price_per_night": 2500, "rating": 4.5},
        {"id": 2, "name": f"{city} Comfort Stay", "address": f"Main Road, {city}", "price_per_night": 1800, "rating": 4.0},
        {"id": 3, "name": f"{city} Budget Inn", "address": f"Market Road, {city}", "price_per_night": 1200, "rating": 3.8},
        {"id": 4, "name": f"{city} Royal Residency", "address": f"Near Bus Station, {city}", "price_per_night": 3200, "rating": 4.6},
        {"id": 5, "name": f"{city} Private Homestay", "address": f"Outskirts of {city}", "price_per_night": 900, "rating": 3.9},
    ][:limit]


async def get_hotel_by_id(hotel_id: int, city: str, limit: int = 5):
    """Fetch a single hotel by its serial number"""
    hotels = await search_hotels(city, limit)
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            return hotel
    return None
