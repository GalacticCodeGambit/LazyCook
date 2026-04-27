from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from EmailService import sendPasswordChangedEmail
from pydantic import BaseModel as _BaseModel


from Auth import (
    Token,
    User,
    UserCreate,
    RefreshRequest,
    LogoutRequest,
    createTokenPair,
    getCurrentUser,
    hashPassword,
    validateEmail,
    validatePassword,
    validateRefreshToken,
    verifyPassword,
    createAccessToken,
)
from Database import (
    createAccount,
    getAccountByEmail,
    deleteRefreshToken,
    deleteAllRefreshTokens,
    deleteAccount,
    updateAccount,
)

from Models import User, Token, UserCreate

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

class UpdateUser(_BaseModel):
    email: str | None = None
    currentPassword: str | None = None
    newPassword: str | None = None

@router.patch("/users/me")
async def updateCurrentUser(
        data: UpdateUser,
        current_user: Annotated[User, Depends(getCurrentUser)]
):
    Account = getAccountByEmail(current_user.email)

    # E-Mail ändern
    if data.email:
        fehler = validateEmail(data.email)
        if fehler:
            raise HTTPException(status_code=400, detail=fehler)
        updateAccount(Account["id"], email=data.email)

    # Passwort ändern
    if data.currentPassword and data.newPassword:
        if not verifyPassword(data.currentPassword, Account["hashedPassword"]):
            raise HTTPException(status_code=401, detail="Falsches Passwort")

        fehler = validatePassword(data.newPassword)
        if fehler:
            raise HTTPException(status_code=400, detail=fehler)

        neuer_hash = hashPassword(data.newPassword)
        updateAccount(Account["id"], password_hash=neuer_hash)

        # NEU: try/catch um echten Fehler zu sehen
        empfaenger_email = data.email if data.email else Account["email"]
        try:
            sendPasswordChangedEmail(empfaenger_email, Account["name"])
        except Exception as e:
            print(f"E-Mail konnte nicht gesendet werden: {e}")

    return {"success": True}
