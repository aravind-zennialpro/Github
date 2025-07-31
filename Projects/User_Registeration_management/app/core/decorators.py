from functools import wraps
from fastapi import Request, HTTPException
from jose import JWTError
from datetime import datetime
from app.core.jwt_handler import decode_token
from app.core.security import is_password_expired
import logging

def jwt_required(func):
    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth:
            raise HTTPException(status_code=401, detail="Missing token")
        token = auth.replace("Bearer ", "")
        try:
            payload = decode_token(token)
            request.state.user = payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return await func(*args, request=request, **kwargs)
    return wrapper

def check_password_expiry(func):
    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        user_data = request.state.user
        last_changed = datetime.fromisoformat(user_data.get("password_last_changed"))
        if is_password_expired(last_changed):
            raise HTTPException(status_code=403, detail="Password expired. Please change your password.")
        return await func(*args, request=request, **kwargs)
    return wrapper

def log_execution_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = datetime.now()
        response = await func(*args, **kwargs)
        duration = (datetime.now() - start).total_seconds() * 1000
        logging.info(f"{func.__name__} executed in {duration:.2f} ms")
        if isinstance(response, dict):
            response["execution_time_ms"] = round(duration, 2)
        return response
    return wrapper
