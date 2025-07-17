from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://bhairocky221:1f5ssAijsZHwtEpm@agenticai.zum19he.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URI)
db = client["fastapi"]
collection = db["items"]
