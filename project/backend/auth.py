"""
auth.py – Authentifizierungslogik (JWT, Passwort-Hashing, Refresh Tokens, Dependencies)
"""

import re
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
from pydantic import BaseModel

from Datenbank import get_konto_by_email, save_refresh_token, get_refresh_token

# ── Konfiguration ──────────────────────────────────────────────
SECRET_KEY = "dein-geheimer-schlüssel-hier-ändern"  # In Produktion: aus Umgebungsvariable laden!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10       # kurze Laufzeit für Access Token
REFRESH_TOKEN_EXPIRE_DAYS = 7          # lange Laufzeit für Refresh Token

# ── Modelle ────────────────────────────────────────────────────
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

# ── Passwort-Hashing ──────────────────────────────────────────
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

# ── Access Token (JWT) ─────────────────────────────────────────
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> str | None:
    """Dekodiert ein JWT und gibt die E-Mail (sub) zurück, oder None."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

# ── Refresh Token ──────────────────────────────────────────────
def create_refresh_token(konto_id: int) -> str:
    """Erstellt einen kryptografisch sicheren Refresh Token und speichert ihn in der DB."""
    token = secrets.token_urlsafe(64)
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    save_refresh_token(konto_id, token, expires_at.isoformat())
    return token

def validate_refresh_token(token: str) -> dict | None:
    """Prüft ob ein Refresh Token gültig und nicht abgelaufen ist. Gibt Konto-Daten zurück."""
    entry = get_refresh_token(token)
    if entry is None:
        return None
    expires_at = datetime.fromisoformat(entry["expires_at"])
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        return None
    return entry

# ── Token-Paar erstellen ──────────────────────────────────────
def create_token_pair(konto: dict) -> Token:
    """Erstellt ein Access + Refresh Token-Paar für ein Konto."""
    access_token = create_access_token(
        data={"sub": konto["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(konto["id"])
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

# ── Validierung ────────────────────────────────────────────────
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

def validate_email(email: str) -> str | None:
    if not EMAIL_RE.match(email):
        return "Ungültige E-Mail-Adresse."
    return None

def validate_password(pw: str) -> str | None:
    if len(pw) < 8:
        return "Passwort muss mindestens 8 Zeichen lang sein."
    if not re.search(r"[A-Z]", pw):
        return "Passwort muss mindestens einen Großbuchstaben enthalten."
    if not re.search(r"[a-z]", pw):
        return "Passwort muss mindestens einen Kleinbuchstaben enthalten."
    if not re.search(r"[0-9]", pw):
        return "Passwort muss mindestens eine Zahl enthalten."
    if not re.search(r"[^A-Za-z0-9]", pw):
        return "Passwort muss mindestens ein Sonderzeichen enthalten."
    return None

# ── Auth-Dependency ────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ungültige Anmeldedaten",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = decode_token(token)
    if email is None:
        raise credentials_exception

    konto = get_konto_by_email(email)
    if konto is None:
        raise credentials_exception

    return User(email=konto["email"], name=konto["name"])