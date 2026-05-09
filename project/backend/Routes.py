from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from EmailService import sendPasswordChangedEmail
from pydantic import BaseModel as _BaseModel


from Auth import (
    createTokenPair,
    getCurrentUser,
    hashPassword,
    validateEmail,
    validatePassword,
    validateRefreshToken,
    verifyPassword,
    createAccessToken,
    createPasswordResetToken,
    validatePasswordResetToken,
)
from Database import (
    createAccount,
    getAccountByEmail,
    deleteRefreshToken,
    deleteAllRefreshTokens,
    deleteAccount,
    updateAccount,
    markResetTokenUsed,
    updateKontoPassword,
    deleteAllRefreshTokens

)

from Models import User, Token, UserCreate, RefreshRequest, LogoutRequest, ForgotPasswordRequest, ResetPasswordRequest, UpdateUser

router = APIRouter()


# ── Auth-Endpunkte ─────────────────────────────────────────────

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

    Account = createAccount(
        email=user.email,
        name=user.name,
        hashedPassword=hashPassword(user.password),
    )
    if Account is None:
        raise HTTPException(status_code=400, detail="E-Mail bereits registriert")

    return User(email=Account["email"], name=Account["name"])


@router.post("/auth/login", response_model=Token)
async def login(formData: Annotated[OAuth2PasswordRequestForm, Depends()]):
    Account = getAccountByEmail(formData.username)
    if not Account or not verifyPassword(formData.password, Account["hashedPassword"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-Mail oder Passwort falsch",
        )
    return createTokenPair(Account)


@router.post("/auth/refresh", response_model=Token)
async def refresh(body: RefreshRequest):
    """Tauscht einen gültigen Refresh Token gegen ein neues Token-Paar."""
    entry = validateRefreshToken(body.refresh_token)
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token ungültig oder abgelaufen",
        )

    # Alten Refresh Token löschen (Rotation – jeder Token ist nur einmal verwendbar)
    deleteRefreshToken(body.refresh_token)

    # Account-Daten für neues Token-Paar zusammenstellen
    Account = {"id": entry["konto_id"], "email": entry["email"]}
    return createTokenPair(Account)


@router.post("/auth/logout")
async def logout(body: LogoutRequest):
    """Löscht den Refresh Token serverseitig → Token wird ungültig."""
    deleteRefreshToken(body.refresh_token)
    return {"detail": "Erfolgreich abgemeldet"}


# ── Geschützte Endpunkte ───────────────────────────────────────

@router.get("/users/me", response_model=User)
async def readCurrentUser(currentUser: Annotated[User, Depends(getCurrentUser)]):
    """Nur mit gültigem Access Token erreichbar."""
    return currentUser


@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
async def deleteCurrentUser(currentUser: Annotated[User, Depends(getCurrentUser)]):
    """Löscht das eigene Account inkl. aller Refresh Tokens (CASCADE)."""
    deleteAccount(currentUser.email)

    # ── Account aktualisieren ────────────────────────────────────────



@router.patch("/users/me")
async def updateCurrentUser(
        data: UpdateUser,
        currentUser: Annotated[User, Depends(getCurrentUser)]
):
    Account = getAccountByEmail(currentUser.email)

    # E-Mail ändern
    if data.email:
        error = validateEmail(data.email)
        if error:
            raise HTTPException(status_code=400, detail=error)
        updateAccount(Account["id"], email=data.email)

    # Passwort ändern
    if data.currentPassword and data.newPassword:
        if not verifyPassword(data.currentPassword, Account["hashedPassword"]):
            raise HTTPException(status_code=400, detail="Aktuelles Passwort ist falsch")

        error = validatePassword(data.newPassword)
        if error:
            raise HTTPException(status_code=400, detail=error)

        newHash = hashPassword(data.newPassword)
        updateAccount(Account["id"], password_hash=newHash)

        # NEU: try/catch um echten Fehler zu sehen
        RecieverEmail = data.email if data.email else Account["email"]
        try:
            sendPasswordChangedEmail(RecieverEmail, Account["name"])
        except Exception as e:
            print(f"E-Mail konnte nicht gesendet werden: {e}")

    return {"success": True}

# ------------ Passwort vergessen ----------------- #

@router.post("/auth/forgot-password")
async def forgotPassword(body: ForgotPasswordRequest):
    """Schritt 1: User gibt E-Mail ein, bekommt Reset-Link per Mail."""
    konto = getAccountByEmail(body.email)

    # Token nur erzeugen wenn Konto existiert – aber IMMER gleiche Antwort senden!
    if konto is not None:
        token = createPasswordResetToken(konto["id"])
        resetLink = f"http://localhost:8000/reset-password?token={token}"
        # TODO: Mail versenden – siehe Hinweis unten
        print(f"[DEV] Reset-Link für {body.email}: {resetLink}")

    return {"detail": "Falls die E-Mail existiert, wurde ein Link versendet."}


@router.post("/auth/reset-password")
async def resetPassword(body: ResetPasswordRequest):
    """Schritt 2: User setzt mit Token aus Mail das neue Passwort."""
    pwError = validatePassword(body.new_password)
    if pwError:
        raise HTTPException(status_code=400, detail=pwError)

    entry = validatePasswordResetToken(body.token)
    if entry is None:
        raise HTTPException(
            status_code=400,
            detail="Link ungültig oder abgelaufen. Bitte neuen anfordern.",
        )

    updateKontoPassword(entry["konto_id"], hashPassword(body.new_password))
    markResetTokenUsed(entry["id"])
    # Sicherheitsmaßnahme: Alle aktiven Sessions ungültig machen
    deleteAllRefreshTokens(entry["konto_id"])

    return {"detail": "Passwort erfolgreich zurückgesetzt."}
