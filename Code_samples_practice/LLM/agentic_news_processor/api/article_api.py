from fastapi import APIRouter, HTTPException, Query
from model.article_model import ArticleModel
from utils.mongo_logger import load_article_store
from bson import ObjectId

router = APIRouter()
article_store  = load_article_store()

@router.get("/articles", response_model = list[ArticleModel])
def get_all_articles():
    results = list (article_store.find()) # All the Records
    return results

@router.get("/articles/get_by_title" , response_model = list[ArticleModel])
def get_article_by_title(title: str = Query(..., min_length=2)):
    query = {"title": {"$regex" : title, "$options": "i"}}
    articles = list (article_store.find(query))  # Filtered Records based on Column / Node
    return articles

@router.get("/articles/get_by_id/{article_id}", response_model = ArticleModel)
def get_article_by_article_id (article_id: str):
    article = article_store.find_one({"article_id" : article_id})
    if not article:
        raise HTTPException(status_code=404, detail="Article Not Found")
    return article

@router.get("/articles/get_by_object_id/{object_id}", response_model = ArticleModel)
def get_article_by_objectid_id (object_id: str):
    article = article_store.find_one({"_id" : ObjectId(object_id)})
    if not article:
        raise HTTPException(status_code=404, detail="Article Not Found")
    return article