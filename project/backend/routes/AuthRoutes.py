"""
routes/auth.py – Authentifizierungs-Endpunkte (Register, Login, Refresh, Logout, Passwort-Reset)
"""

import logging
import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.Auth import validateEmail, validatePassword, verifyPassword, hashPassword
from dao import AccountDAO
from services import AuthService
from services.EmailService import sendPasswordChangedEmail, sendPasswordResetEmail
from core.Models import (
    User,
    Token,
    UserCreate,
    RefreshRequest,
    LogoutRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from services import UserService

logger = logging.getLogger(__name__)

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:8000")

router = APIRouter()


@router.post("/auth/register", response_model=User)
async def register(user: UserCreate):
    if not user.name.strip():
        raise HTTPException(status_code=400, detail="Name darf nicht leer sein.")
    emailError = validateEmail(user.email)
    if emailError:
        raise HTTPException(status_code=400, detail=emailError)
    pwError = validatePassword(user.password)
    if pwError:
        raise HTTPException(status_code=400, detail=pwError)

    account = UserService.register(user.email, user.name, user.password)
    if account is None:
        raise HTTPException(status_code=400, detail="E-Mail bereits registriert")

    return User(email=account["email"], name=account["name"])


@router.post("/auth/login", response_model=Token)
async def login(formData: Annotated[OAuth2PasswordRequestForm, Depends()]):
    account = AccountDAO.getAccountByEmail(formData.username)
    if not account or not verifyPassword(formData.password, account["hashedPassword"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-Mail oder Passwort falsch",
        )
    return AuthService.createTokenPair(account)


@router.post("/auth/refresh", response_model=Token)
async def refresh(body: RefreshRequest):
    """Tauscht einen gültigen Refresh Token gegen ein neues Token-Paar."""
    entry = AuthService.validateRefreshToken(body.refresh_token)
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token ungültig oder abgelaufen",
        )
    AccountDAO.deleteRefreshToken(body.refresh_token)
    account = {"id": entry["AccountID"], "email": entry["email"]}
    return AuthService.createTokenPair(account)


@router.post("/auth/logout")
async def logout(body: LogoutRequest):
    """Löscht den Refresh Token serverseitig."""
    AccountDAO.deleteRefreshToken(body.refresh_token)
    return {"detail": "Erfolgreich abgemeldet"}


@router.post("/auth/forgot-password")
async def forgotPassword(body: ForgotPasswordRequest):
    """Schritt 1: User gibt E-Mail ein, bekommt Reset-Link per Mail."""
    konto = AccountDAO.getAccountByEmail(body.email)
    if konto is not None:
        token = AuthService.createPasswordResetToken(konto["id"])
        resetLink = f"{FRONTEND_URL}/reset-password?token={token}"
        try:
            sendPasswordResetEmail(body.email, konto["name"], resetLink)
        except Exception as e:
            logger.warning("Reset-Mail konnte nicht gesendet werden: %s", e)
    return {"detail": "Falls die E-Mail existiert, wurde ein Link versendet."}


@router.post("/auth/reset-password")
async def resetPassword(body: ResetPasswordRequest):
    """Schritt 2: User setzt mit Token aus Mail das neue Passwort."""
    pwError = validatePassword(body.new_password)
    if pwError:
        raise HTTPException(status_code=400, detail=pwError)

    entry = AuthService.validatePasswordResetToken(body.token)
    if entry is None:
        raise HTTPException(
            status_code=400,
            detail="Link ungültig oder abgelaufen. Bitte neuen anfordern.",
        )

    AccountDAO.updateKontoPassword(entry["kontoID"], hashPassword(body.new_password))
    AccountDAO.markResetTokenUsed(entry["id"])
    AccountDAO.deleteAllRefreshTokens(entry["kontoID"])

    konto = AccountDAO.getAccountById(entry["kontoID"])
    if konto is not None:
        try:
            sendPasswordChangedEmail(konto["email"], konto["name"])
        except Exception as e:
            logger.warning("Bestätigungsmail konnte nicht gesendet werden: %s", e)

    return {"detail": "Passwort erfolgreich zurückgesetzt."}
