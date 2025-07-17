from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime

from models import Route, Booking
from schemas import BookingRequest

router = APIRouter()

@router.get("/routes")
async def get_routes():
    return await Route.find_all().to_list()

@router.post("/admin/update_routes")
async def update_routes(new_routes: List[Route]):
    await Route.delete_all()
    for r in new_routes:
        await r.insert()
    return {"message": "Routes updated successfully", "total": len(new_routes)}

@router.post("/book")
async def book_ticket(request: BookingRequest):
    route = await Route.get(request.route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Invalid Route ID")

    new_booking = Booking(
        passenger_name=request.passenger_name,
        phone=request.phone,
        route_id=str(route.id),
        timestamp=datetime.utcnow().isoformat()
    )
    await new_booking.insert()
    return {
        "message": "Booking successful. Have a nice journey!",
        "ticket": new_booking
    }

@router.get("/bookings")
async def get_all_bookings():
    return await Booking.find_all().to_list()
