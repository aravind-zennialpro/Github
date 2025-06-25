from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Attendance
from schemas import AttendanceCreate, AttendanceOut

router = APIRouter(prefix="/attendance", tags=["Attendance"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AttendanceOut)
def record_attendance(att: AttendanceCreate, db: Session = Depends(get_db)):
    if att.action not in ["checkin", "checkout"]:
        raise HTTPException(status_code=400, detail="Invalid action.")
    record = Attendance(employee_id=att.employee_id, action=att.action)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/all", response_model=list[AttendanceOut])
def get_all_records(db: Session = Depends(get_db)):
    return db.query(Attendance).order_by(Attendance.timestamp.desc()).all()
