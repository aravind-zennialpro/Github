# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine, Base
from fastapi import Path

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add a route (admin)
@app.post("/add_route", response_model=schemas.RouteOut)
def add_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    db_route = models.Route(**route.dict())
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

@app.put("/update_route/{route_id}", response_model=schemas.RouteOut)
def update_route(
    route_id: int = Path(..., description="ID of the route to update"),
    route_data: schemas.RouteUpdate = ...,
    db: Session = Depends(get_db)
):
    route = db.query(models.Route).filter(models.Route.id == route_id).first()

    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    # Update only provided fields
    if route_data.source is not None:
        route.source = route_data.source
    if route_data.destination is not None:
        route.destination = route_data.destination
    if route_data.fare is not None:
        route.fare = route_data.fare
    if route_data.departure_time is not None:
        route.departure_time = route_data.departure_time

    db.commit()
    db.refresh(route)
    return route

# Get all routes
@app.get("/routes", response_model=list[schemas.RouteOut])
def get_routes(db: Session = Depends(get_db)):
    return db.query(models.Route).all()

# Book a ticket
@app.post("/book", response_model=schemas.BookingOut)
def book_ticket(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    route = db.query(models.Route).filter(models.Route.id == booking.route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    new_booking = models.Booking(**booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

# Get all bookings
@app.get("/bookings", response_model=list[schemas.BookingOut])
def get_all_bookings(db: Session = Depends(get_db)):
    return db.query(models.Booking).all()
