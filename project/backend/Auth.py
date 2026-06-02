"""
Auth.py – Authentifizierungslogik (JWT, Passwort-Hashing, Refresh Tokens, Dependencies)
"""

import re
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt

import hashlib

PASSWORD_RESET_EXPIRE_MINUTES = 30

from Models import Token, User

from Database import getAccountByEmail, saveRefreshToken, getRefreshToken

# ── Konfiguration ──────────────────────────────────────────────
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY ist nicht gesetzt!")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10  # kurze Laufzeit für Access Token
refreshToken_EXPIRE_DAYS = 7  # lange Laufzeit für Refresh Token


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


# ── Refresh Token ──────────────────────────────────────────────
def createRefreshToken(konto_id: int) -> str:
    """Erstellt einen kryptografisch sicheren Refresh Token und speichert ihn in der DB."""
    token = secrets.token_urlsafe(64)
    expiresAt = datetime.now(timezone.utc) + timedelta(days=refreshToken_EXPIRE_DAYS)
    saveRefreshToken(konto_id, token, expiresAt.isoformat())
    return token


def validateRefreshToken(token: str) -> dict | None:
    """Prüft ob ein Refresh Token gültig und nicht abgelaufen ist. Gibt Konto-Daten zurück."""
    entry = getRefreshToken(token)
    if entry is None:
        return None
    expiresAt = datetime.fromisoformat(entry["expiresAt"])
    if expiresAt.tzinfo is None:
        expiresAt = expiresAt.replace(tzinfo=timezone.utc)
    if expiresAt < datetime.now(timezone.utc):
        return None
    return entry


# ── Token-Paar erstellen ──────────────────────────────────────
def createTokenPair(konto: dict) -> Token:
    """Erstellt ein Access + Refresh Token-Paar für ein Konto."""
    access_token = createAccessToken(
        data={"sub": konto["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refreshToken = createRefreshToken(konto["id"])
    return Token(
        access_token=access_token, refresh_token=refreshToken, token_type="bearer"
    )


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

    konto = getAccountByEmail(email)
    if konto is None:
        raise credentials_exception

    return User(email=konto["email"], name=konto["name"])


# --- Reset Password --- #


def hashResetToken(token: str) -> str:
    """SHA-256 Hash – für Reset-Tokens reicht das, sie sind ohnehin hochentropisch."""
    return hashlib.sha256(token.encode()).hexdigest()


def createPasswordResetToken(kontoId: int) -> str:
    """Generiert Klartext-Token (geht per Mail) und speichert nur den Hash in der DB."""
    from Database import savePasswordResetToken

    token = secrets.token_urlsafe(48)
    expiresAt = datetime.now(timezone.utc) + timedelta(
        minutes=PASSWORD_RESET_EXPIRE_MINUTES
    )
    savePasswordResetToken(kontoId, hashResetToken(token), expiresAt.isoformat())
    return token


def validatePasswordResetToken(token: str) -> dict | None:
    from Database import getPasswordResetToken

    entry = getPasswordResetToken(hashResetToken(token))
    if entry is None or entry["usedAt"] is not None:
        return None
    expiresAt = datetime.fromisoformat(entry["expiresAt"])
    if expiresAt.tzinfo is None:
        expiresAt = expiresAt.replace(tzinfo=timezone.utc)
    if expiresAt < datetime.now(timezone.utc):
        return None
    return entry
