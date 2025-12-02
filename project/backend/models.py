from pydantic import BaseModel, EmailStr
from datetime import datetime

# Pydantic Models
class UserSignUpIn(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr

class SessionResponse(BaseModel):
    session_token: str
    user: UserResponse
    expires_at: datetime
