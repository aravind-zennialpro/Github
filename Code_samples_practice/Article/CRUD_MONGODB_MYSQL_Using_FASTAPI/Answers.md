## ❓ Frequently Asked Questions (FAQ)

Here are some commonly asked questions about this FastAPI project using MongoDB and MySQL:

---

### 1. What is the role of `motor` in the MongoDB integration?

**A:** `motor` is an **asynchronous MongoDB driver** for Python. It allows FastAPI to interact with MongoDB using `async` and `await`, enabling non-blocking I/O and improved performance in web applications.

---

### 2. Why do we use `ObjectId` in the MongoDB router?

**A:** MongoDB stores document IDs as `ObjectId` types. When retrieving or querying documents by ID, we must **convert the string ID** (received from the client) into an `ObjectId` using:
```python
from bson import ObjectId
object_id = ObjectId(item_id)
```

---

### 3. What does ```Base.metadata.create_all(bind=engine)``` do in ```main.py```?

**A:** This line tells SQLAlchemy to create all tables defined in the models (```MySQLItem``` in this case) using the specified database engine. It's typically used during the initial setup to ensure the database schema exists.

---

### 4. How are MongoDB and MySQL schemas different in this project?

**A:** MongoDB: Uses only Pydantic models (```mongo_schema.py```) for request/response validation, as MongoDB is schema-less.

MySQL: Uses SQLAlchemy models (```mysql_model.py```) to define table structures and Pydantic schemas (```mysql_schema.py```) to validate input/output data.


---

###  5. How can I test both MongoDB and MySQL endpoints?

**A:** After running the app using:

```
uvicorn app.main:app --reload
```
Go to: http://localhost:8000/docs
This opens the Swagger UI, where you can test:

```/mongo/item/``` - MongoDB routes

```/mysql/item/``` - MySQL routes

---

### 6. What is the purpose of separating files into ```schemas```, ```models```, ```routers```, and ```db``` folders?

**A:** This structure follows FastAPI best practices for clean, maintainable code:

* ```schemas/```: Pydantic models for request and response data.

* ```models/```: SQLAlchemy models (for MySQL).

* ```routers/```: Route definitions for endpoints.

* ```db/```: Database connection and config files.

It helps in organizing code logically and makes it easier to scale the project.

---

### 7. Why do we use ```orm_mode = True``` in Pydantic schemas?

**A:** Setting ```orm_mode = True``` in Pydantic models allows them to **serialize ORM** objects (like SQLAlchemy models) into valid API responses. Without this, FastAPI wouldn't know how to convert SQLAlchemy objects into JSON.

---

### 8. What’s the difference between MongoDB’s ```insert_one()``` and SQLAlchemy’s ```add()``` + ```commit()```?

**A:** MongoDB (```insert_one()```): Directly inserts a document into the collection.

MySQL (SQLAlchemy): Requires creating an object, adding it to the session with ```add()```, and saving it to the DB using ```commit()```.

This difference highlights how **NoSQL** and **SQL operations** are handled in code.

---

### 9. How does FastAPI handle async and sync DB operations together in this project?

**A:** FastAPI supports both async (for MongoDB using ```motor```) and **sync** (for MySQL using SQLAlchemy) routes. It internally uses **Starlette and asyncio** to manage concurrency, so both types can coexist in a single app without conflict.

---

### 10. Can we extend this project to include update and delete routes?

**A:** Yes! Here's how:

**MongoDB - Update Example**
```

@router.put("/item/{item_id}")
async def update_item(item_id: str, item: MongoItem):
    object_id = ObjectId(item_id)
    result = await collection.update_one({"_id": object_id}, {"$set": item.dict()})
    return {"updated_count": result.modified_count}
```
**MySQL - Delete Example
**
```
@router.delete("/item/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(MySQLItem).filter(MySQLItem.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
        return {"detail": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
```