from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# In-memory activity log
activity_log = []

# Request body model
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(data: LoginRequest):
    if data.username == "admin" and data.password == "1234":
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success",
            "message": "Login successful",
            "token": "abcd1234"
        }
        activity_log.append(log_entry)
        return log_entry
    else:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "error",
            "message": "Invalid credentials"
        }
        activity_log.append(log_entry)
        raise HTTPException(status_code=401, detail=log_entry)

@app.get("/activities")
async def get_activities():
    return activity_log
