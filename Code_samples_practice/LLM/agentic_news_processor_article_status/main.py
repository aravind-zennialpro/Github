from fastapi import FastAPI
from api.article_api import router as articles_router

app = FastAPI (title = "Agentic Article Processor")
app.include_router (articles_router)