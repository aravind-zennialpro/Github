# to save the user data in Mysql
# we have to create databse i.e: CREATE DATABSE user_register
# we want a detailed table to save the table
# run_create_table.py

from app.db.mysql import engine
from app.db.models import Base

# Create all tables in the database
Base.metadata.create_all(bind=engine)