from fastapi import FastAPI
from routers import mongo_router, mysql_router
from db.mysql import Base, engine

# Create MySQL Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI CRUD with MongoDB and MySQL")

# Include Routes
app.include_router(mongo_router.router)
app.include_router(mysql_router.router)
