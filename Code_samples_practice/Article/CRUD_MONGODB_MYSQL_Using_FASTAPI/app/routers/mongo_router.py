from fastapi import APIRouter, HTTPException
from schemas.mongo_schema import MongoItem
from db.mongodb import collection
from bson import ObjectId

router = APIRouter(prefix="/mongo")

@router.post("/item/")
async def create_item(item: MongoItem):
    result = await collection.insert_one(item.dict())
    return {"id": str(result.inserted_id)}

@router.get("/mongo/item/{item_id}", response_model=MongoItem)
async def read_item(item_id: str):
    try:
        object_id = ObjectId(item_id)  # ✅ Convert to MongoDB ObjectId
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    item = await collection.find_one({"_id": object_id})
    if item:
        item["id"] = str(item["_id"])  # ✅ Convert ObjectId to string for response
        return item

    raise HTTPException(status_code=404, detail="Item not found")