from pydantic import BaseModel, EmailStr
from datetime import datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class User(BaseModel):
    email: str
    name: str


class UserCreate(BaseModel):
    email: str
    name: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class UpdateUser(BaseModel):
    email: str | None = None
    currentPassword: str | None = None
    newPassword: str | None = None


class IngredientSearch(BaseModel):
    name: str
    amount: float
    unit: str


class RecipeSearchRequest(BaseModel):
    zutaten: list[IngredientSearch]
    servings: int = 1
    index: int = 0
