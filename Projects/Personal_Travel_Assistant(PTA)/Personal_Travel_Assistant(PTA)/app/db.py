# app/db.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://bhairocky221:1f5ssAijsZHwtEpm@agenticai.zum19he.mongodb.net/")
DB_NAME = os.getenv("DB_NAME", "pta_db")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]

# Collections fom db
bookings_collection = db["bookings"]
