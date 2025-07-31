import motor.motor_asyncio
from app.core.config import MONGO_URI

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
mongodb = client.user_register
user_collection = mongodb.get_collection("users")
