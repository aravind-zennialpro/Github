from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

MYSQL_URI = "mysql+mysqlconnector://root:Aravind21081998@localhost/fastapi"
engine = create_engine(MYSQL_URI)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
