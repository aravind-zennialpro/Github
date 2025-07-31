from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import MYSQL_URI

engine = create_engine(MYSQL_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
