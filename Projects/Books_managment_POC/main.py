from fastapi import FastAPI, HTTPException
from models import Book
from database import books_db

app = FastAPI()

# GET all books
@app.get("/books")
def get_books():
    return books_db

# GET book by ID
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# POST a new book
@app.post("/books")
def add_book(book: Book):
    # Check for duplicate ID
    for b in books_db:
        if b.id == book.id:
            raise HTTPException(status_code=400, detail="Book ID already exists")
    books_db.append(book)
    return {"message": "Book added successfully"}

# DELETE a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            books_db.pop(index)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

# (Optional) UPDATE a book
@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            books_db[index] = updated_book
            return {"message": "Book updated successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
