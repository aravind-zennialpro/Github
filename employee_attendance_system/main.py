from fastapi import FastAPI
from database import Base, engine
from routers import attendance

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(attendance.router)

@app.get("/")
def home():
    return {"message": "Employee Attendance API is running"}
