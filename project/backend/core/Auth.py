"""
Auth.py – Kryptographie, Validierung, JWT-Encoding und FastAPI-Dependency
"""
import re
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt

from core.Models import User
from dao import AccountDAO

# ── Konfiguration ──────────────────────────────────────────────
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY ist nicht gesetzt!")


# ── Passwort-Hashing ──────────────────────────────────────────
def hashPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verifyPassword(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


# ── Access Token (JWT) ─────────────────────────────────────────
def createAccessToken(data: dict, expires_delta: timedelta | None = None) -> str:
    toEncode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    toEncode.update({"exp": expire})
    return jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)


def decodeToken(token: str) -> str | None:
    """Dekodiert ein JWT und gibt die E-Mail (sub) zurück, oder None."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


# ── Validierung ────────────────────────────────────────────────
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validateEmail(email: str) -> str | None:
    if not EMAIL_RE.match(email):
        return "Ungültige E-Mail-Adresse."
    return None


def validatePassword(pw: str) -> str | None:
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


async def getCurrentUser(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Ungültige Anmeldedaten",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = decodeToken(token)
    if email is None:
        raise credentials_exception

    konto = AccountDAO.getAccountByEmail(email)
    if konto is None:
        raise credentials_exception

    return User(email=konto["email"], name=konto["name"])
