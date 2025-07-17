# app/models/mongo_model.py

from db.mongodb import collection
from bson import ObjectId

async def get_item_by_id(item_id: str):
    return await collection.find_one({"_id": ObjectId(item_id)})

async def create_item(item_data: dict):
    result = await collection.insert_one(item_data)
    return str(result.inserted_id)

async def update_item(item_id: str, update_data: dict):
    await collection.update_one({"_id": ObjectId(item_id)}, {"$set": update_data})
    return True

async def delete_item(item_id: str):
    await collection.delete_one({"_id": ObjectId(item_id)})
    return True
