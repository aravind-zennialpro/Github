from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class UserRegister(BaseModel):
    username: str
    first_name: str
    last_name: str
    dob: date
    doj: date
    address: str
    comment: Optional[str]
    is_active: bool = True
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class ChangeUsernameRequest(BaseModel):
    new_username: str

class ForgotPasswordRequest(BaseModel):
    username: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
class logout(BaseModel):
    token: str
    username: str