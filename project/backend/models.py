from pydantic import BaseModel, EmailStr
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    email: str
    name: str

class UserCreate(BaseModel):
    email: str
    name: str
    password: str