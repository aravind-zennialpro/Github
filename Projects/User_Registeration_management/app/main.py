from fastapi import FastAPI
from app.routes import auth_routes
from app.core.logger import setup_logging

app = FastAPI(title="User Registration Module API")
setup_logging()
app.include_router(auth_routes.router)
