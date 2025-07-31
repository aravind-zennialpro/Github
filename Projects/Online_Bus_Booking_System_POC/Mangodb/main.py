from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from dotenv import load_dotenv

from models import Route, Booking
from routes import router as api_router

app = FastAPI()

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

@app.on_event("startup")
async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(
        database=client.get_default_database(),
        document_models=[Route, Booking]
    )

app.include_router(api_router)
