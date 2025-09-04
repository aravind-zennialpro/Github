# app/services/bus_service.py
import asyncio
from datetime import datetime, timedelta

async def search_buses(from_city: str, to_city: str, depart_date: str = None):
    """
    Demo/mock bus search for APSRTC, TSRTC, and Private Travels.
    Returns 5 sample bus options WITH SERIAL NUMBERS.
    """
    base_time = datetime.now().replace(minute=0, second=0, microsecond=0)

    buses = [
        {
            "id": 1,
            "operator": "APSRTC Super Luxury",
            "departure_time": (base_time + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            "arrival_time": (base_time + timedelta(hours=6)).strftime("%Y-%m-%d %H:%M"),
            "duration": "4h",
            "price": 500,
            "bus_type": "Non-AC Seater"
        },
        {
            "id": 2,
            "operator": "TSRTC Rajadhani",
            "departure_time": (base_time + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
            "arrival_time": (base_time + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M"),
            "duration": "4h",
            "price": 650,
            "bus_type": "AC Seater"
        },
        {
            "id": 3,
            "operator": "TSRTC Garuda Plus",
            "departure_time": (base_time + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
            "arrival_time": (base_time + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M"),
            "duration": "4h",
            "price": 800,
            "bus_type": "AC Sleeper"
        },
        {
            "id": 4,
            "operator": "Private Travels - Orange",
            "departure_time": (base_time + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M"),
            "arrival_time": (base_time + timedelta(hours=11)).strftime("%Y-%m-%d %H:%M"),
            "duration": "4h",
            "price": 950,
            "bus_type": "AC Sleeper"
        },
        {
            "id": 5,
            "operator": "Private Travels - VRL",
            "departure_time": (base_time + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M"),
            "arrival_time": (base_time + timedelta(hours=13)).strftime("%Y-%m-%d %H:%M"),
            "duration": "4h",
            "price": 1100,
            "bus_type": "AC Multi-Axle Sleeper"
        }
    ]

    await asyncio.sleep(0.1)  # simulate DB/API delay
    return buses


async def get_bus_by_id(bus_id: int, from_city: str, to_city: str, depart_date: str = None):
    """
    Fetch a single bus by its serial number.
    """
    buses = await search_buses(from_city, to_city, depart_date)
    for bus in buses:
        if bus["id"] == bus_id:
            return bus
    return None
