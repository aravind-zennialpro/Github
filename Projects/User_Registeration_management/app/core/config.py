import os
from dotenv import load_dotenv
# loading .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://bhairocky221:1f5ssAijsZHwtEpm@agenticai.zum19he.mongodb.net/")
MYSQL_URI = os.getenv("MYSQL_URI", "mysql+mysqlconnector://root:Aravind21081998@localhost/user_register")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
