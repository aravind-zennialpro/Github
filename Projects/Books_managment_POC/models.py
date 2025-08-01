from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str
    type: str
    pages: int
