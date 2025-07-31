from pydantic import BaseModel
from datetime import datetime

class AttendanceCreate(BaseModel):
    employee_id: str
    action: str  # "checkin" or "checkout"

class AttendanceOut(BaseModel):
    id: int
    employee_id: str
    action: str
    timestamp: datetime

    class Config:
        orm_mode = True
