from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.mysql import SessionLocal
from models.mysql_model import MySQLItem
from schemas.mysql_schema import MySQLItemCreate, MySQLItemOut

router = APIRouter(prefix="/mysql")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/item/", response_model=MySQLItemOut)
def create_item(item: MySQLItemCreate, db: Session = Depends(get_db)):
    db_item = MySQLItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/item/{item_id}", response_model=MySQLItemOut)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(MySQLItem).filter(MySQLItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
