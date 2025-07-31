from pydantic import BaseModel

class MySQLItemCreate(BaseModel):
    name: str
    description: str

class MySQLItemOut(MySQLItemCreate):
    id: int
