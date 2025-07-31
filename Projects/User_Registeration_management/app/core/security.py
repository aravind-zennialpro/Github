import bcrypt
from datetime import datetime, timedelta
from typing import List
import jwt

SECRET_KEY = "super-secret-reset-key"
ALGORITHM = "HS256"

# Hashing a password using bcrypt to storing the password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

# Checkingd if password matches hashed versions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Checkingd if password was used earlier or before
def is_password_reused(new_password: str, previous_passwords: List[str]) -> bool:
    return any(verify_password(new_password, old) for old in previous_passwords)

# Checking if password expired or outdated (after 30 days)
def is_password_expired(last_changed: datetime) -> bool:
    return (datetime.utcnow() - last_changed).days > 30

def create_reset_token(username: str, expires_delta=timedelta(hours=24)):
    expire = datetime.utcnow() + expires_delta
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None