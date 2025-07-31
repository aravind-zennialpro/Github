# ✅ CRUD Operations on MongoDB and MySQL using FastAPI

This project demonstrates how to build RESTful CRUD APIs using **FastAPI** with both **MongoDB** (NoSQL) and **MySQL** (SQL) databases. You'll learn how to connect, perform CRUD operations, and organize your project structure effectively.

---

## 🌐 Project Structure

```bash
.📂 CRUD_MONGODB_MYSQL_Using_FASTAPI
️|──📂 app/
|    |──📂 db/
|    |    |── mongodb.py
|    |    |── mysql.py
|    |──📂 models/
|    |    |── Mongo_model.py
|    |    |── mysql_model.py
|    |──📂 routers/
|    |    |── mongo_router.py
|    |    |── mysql_router.py
|    |──📂 schemas/
|    |    |── mongo_schema.py
|    |    |── mysql_schema.py
|    |──📂 .venv/
|    |      |── .env
|    |── main.py
|    |── requirements.txt
```

---

## 🔧 Installation

```
cd CRUD_MONGODB_MYSQL_Using_FASTAPI
conda activate <env>
pip install -r requirements.txt
```

## 🛢 Databases
```
MONGO_URL=mongodb://localhost:27017
MYSQL_URL=mysql+pymysql://username:password@localhost/dbname
```

---

## 📖 Requirements.txt

```
fastapi
uvicorn
motor
pymongo
sqlalchemy
pydantic
pymysql
python-dotenv
```

---

## 📊 MongoDB Setup

### `app/db/mongodb.py`

```python
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL= "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["fastapi"]
collection = db["items"]

```

### `app/schemas/mongo_schema.py`

```python
from pydantic import BaseModel

class MongoItem(BaseModel):
    id: str
    name: str
    description: str

    class Config:
        orm_mode = True

```

### `app/routers/mongo_router.py`

```python
from fastapi import APIRouter, HTTPException
from schemas.mongo_schema import MongoItem
from db.mongodb import collection
from bson import ObjectId

router = APIRouter(prefix="/mongo")

@router.post("/item/")
async def create_item(item: MongoItem):
    result = await collection.insert_one(item.dict())
    return {"id": str(result.inserted_id)}

@router.get("/mongo/item/{item_id}", response_model=MongoItem)
async def read_item(item_id: str):
    try:
        object_id = ObjectId(item_id)  # ✅ Convert to MongoDB ObjectId
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    item = await collection.find_one({"_id": object_id})
    if item:
        item["id"] = str(item["_id"])  # ✅ Convert ObjectId to string for response
        return item

    raise HTTPException(status_code=404, detail="Item not found")
```

---

## 📊 MySQL Setup

### `app/db/mysql.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

MYSQL_URL = "mysql+pymysql://username:password@localhost/dbname"
engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

```

### `app/models/mysql_model.py`

```python
from sqlalchemy import Column, Integer, String
from db.mysql import Base

class MySQLItem(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String(255))

```

### `app/schemas/mysql_schema.py`

```python
from pydantic import BaseModel

class MySQLItemCreate(BaseModel):
    name: str
    description: str

class MySQLItemOut(MySQLItemCreate):
    id: int
```

### `app/routers/mysql_router.py`

```python
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

```

---

## 📆 Main Entry

### `main.py`

```python
from fastapi import FastAPI
from routers import mongo_router, mysql_router
from db.mysql import Base, engine

# Create MySQL Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI CRUD with MongoDB and MySQL")

# Include Routes
app.include_router(mongo_router.router)
app.include_router(mysql_router.router)

```

---

## 🌐 Run the Project

```
uvicorn app.main:app --reload
```

Visit Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📊 Conclusion

This full-stack implementation demonstrates how you can combine FastAPI with both MongoDB and MySQL, enabling flexible API development across relational and document-oriented databases. Great for hybrid backends or comparing DB strategies.

---

## ❓ Frequently Asked Questions (FAQ)

1. What is the role of motor in the MongoDB integration?
2. Why do we use ObjectId in the MongoDB router?
3. What does Base.metadata.create_all(bind=engine) do in main.py?
4. How are MongoDB and MySQL schemas different in this project?
5. How can I test both MongoDB and MySQL endpoints?
6.  What is the purpose of separating files into schemas, models, routers, and db folders?
7.  Why do we use orm_mode = True in Pydantic schemas?
8.  What’s the difference between MongoDB’s insert_one() and SQLAlchemy’s add() + commit()?
9.  How does FastAPI handle async and sync DB operations together in this project?
10. Can we extend this project to include update and delete routes?
---
