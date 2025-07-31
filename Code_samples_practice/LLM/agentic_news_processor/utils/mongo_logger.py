import os
import datetime
from pymongo import MongoClient # pip install pymongo
from utils.logger import get_logger

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://bhairocky221:1f5ssAijsZHwtEpm@agenticai.zum19he.mongodb.net/")
DB_NAME = "resume_manager"
COLLECTION_NAME = "staged_articles"

logger = get_logger("mongo_logger")

try:
    client = MongoClient(MONGO_URI) # Connect to Mongo Cluster -  Local or Cloud Install. As per URI
    db = client[DB_NAME] # Cluster - Database
    article_store = db[COLLECTION_NAME] # - Cluster - Database - Table {Collection}
except Exception as e:
    logger.error(f"MongoDB connection failed: {e}")
    client = None
    article_store = None

def log_article_to_mongo(article_data: dict, status: str): # Failed or Success
    if article_store is None:
        logger.error("MongoDB not connected. Skipping article log.")
        return

    try:
        article_data["processing_status"] = status
        article_data["timestamp"] = datetime.datetime.utcnow()
        article_store.insert_one(article_data)
        logger.info(f"Logged article {article_data.get('article_id')} with status '{status}'")
    except Exception as e:
        logger.error(f"Failed to log article to MongoDB: {e}")


def load_article_store():    
    return article_store