from fastapi import FastAPI
from app.routes.search_routes import router as search_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Personal Travel Assistant")

app.include_router(search_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Personal Travel Assistant API !."}
