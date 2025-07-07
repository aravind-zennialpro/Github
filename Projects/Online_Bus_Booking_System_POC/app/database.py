# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file
SQLALCHEMY_DATABASE_URL = "sqlite:///C:/Github/Full stack Agentic AI Training Session/Projects/Online_Bus_Booking_System_POC/app/database/booking.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# saving routes the bus travel list
#ROUTES = [
#   route(1, "Hyderabad","Kodad", 340,"7:00 PM"),
#   route(2, "Hyderabad","Vijayawada", 520,"7:30 PM"),
#     route(3, "Hyderabad","Amalapuram", 730,"8:00 PM"),
#     route(4, "Hyderabad","Kakinada", 910,"8:45 PM"),
#     route(5, "Hyderabad","Vizag", 1020,"8:30 PM"),
#     route(6, "Hyderabad","Tirupathi",1116, "9:10 PM"),
#     route(7, "Hyderabad","Ongole", 890,"9:25 PM"),
#     route(8, "Ongole","Nellore", 220,"10:00 PM"),
#     route(9, "Vijayawada","Vizag", 890,"11:30 PM")
# ]

# # stores the all bookings
# BOOKINGS = []