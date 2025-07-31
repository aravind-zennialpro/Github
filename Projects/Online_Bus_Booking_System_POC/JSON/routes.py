from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime

from schemas import BookingRequest
from utils import load_json_file, save_json_file

router = APIRouter()

ROUTES_FILE = "routes.json"
BOOKING_FILE = "bookings.json"

@router.get("/routes")
def get_routes():
    return load_json_file(ROUTES_FILE)

@router.post("/book")
def book_ticket(request: BookingRequest):
    routes = load_json_file(ROUTES_FILE)
    bookings = load_json_file(BOOKING_FILE)

    route = next((r for r in routes if r["id"] == request.route_id), None)
    if not route:
        raise HTTPException(status_code=404, detail="Invalid Route...")

    booking_id = len(bookings) + 1
    new_booking = {
        "id": booking_id,
        "passenger_name": request.passenger_name,
        "phone": request.phone,
        "route": route,
        "timestamp": datetime.utcnow().isoformat()
    }

    bookings.append(new_booking)
    save_json_file(BOOKING_FILE, bookings)

    return {
        "message": "Booking successful. Have a nice journey!",
        "ticket": new_booking
    }

@router.get("/bookings")
def get_all_bookings():
    return load_json_file(BOOKING_FILE)

@router.post("/admin/update_routes")
def update_routes(new_routes: List[dict]):
    save_json_file(ROUTES_FILE, new_routes)
    return {
        "message": "Routes updated successfully",
        "total": len(new_routes)
    }
