"""
auth_service.py – Token-Orchestrierung (Refresh Tokens, Password Reset Tokens, Token-Paare)
"""
import secrets
import hashlib
from datetime import datetime, timedelta, timezone

from core.Auth import createAccessToken, ACCESS_TOKEN_EXPIRE_MINUTES
from core.Models import Token
from dao import AccountDAO

REFRESH_TOKEN_EXPIRE_DAYS = 7
PASSWORD_RESET_EXPIRE_MINUTES = 30


def createTokenPair(konto: dict) -> Token:
    """Erstellt ein Access + Refresh Token-Paar für ein Konto."""
    access_token = createAccessToken(
        data={"sub": konto["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = createRefreshToken(konto["id"])
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


def createRefreshToken(konto_id: int) -> str:
    token = secrets.token_urlsafe(64)
    expiresAt = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    AccountDAO.saveRefreshToken(konto_id, token, expiresAt.isoformat())
    return token


def validateRefreshToken(token: str) -> dict | None:
    """Prüft ob ein Refresh Token gültig und nicht abgelaufen ist."""
    entry = AccountDAO.getRefreshToken(token)
    if entry is None:
        return None
    expiresAt = datetime.fromisoformat(entry["expiresAt"])
    if expiresAt.tzinfo is None:
        expiresAt = expiresAt.replace(tzinfo=timezone.utc)
    if expiresAt < datetime.now(timezone.utc):
        return None
    return entry


def createPasswordResetToken(kontoId: int) -> str:
    """Generiert Klartext-Token (geht per Mail) und speichert nur den Hash in der DB."""
    token = secrets.token_urlsafe(48)
    expiresAt = datetime.now(timezone.utc) + timedelta(minutes=PASSWORD_RESET_EXPIRE_MINUTES)
    AccountDAO.savePasswordResetToken(kontoId, hashResetToken(token), expiresAt.isoformat())
    return token


def validatePasswordResetToken(token: str) -> dict | None:
    entry = AccountDAO.getPasswordResetToken(hashResetToken(token))
    if entry is None or entry["usedAt"] is not None:
        return None
    expiresAt = datetime.fromisoformat(entry["expiresAt"])
    if expiresAt.tzinfo is None:
        expiresAt = expiresAt.replace(tzinfo=timezone.utc)
    if expiresAt < datetime.now(timezone.utc):
        return None
    return entry


def hashResetToken(token: str) -> str:
    """SHA-256 Hash – für Reset-Tokens reicht das, sie sind ohnehin hochentropisch."""
    return hashlib.sha256(token.encode()).hexdigest()
