from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth import (
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
from project.backend.Database import (
    createKonto,
    getKontoByEmail,
    deleteRefreshToken,
    deleteAllRefreshTokens,
    deleteKonto,
)

router = APIRouter()


# ── Auth-Endpunkte ─────────────────────────────────────────────

@router.post("/auth/register", response_model=User)
async def register(user: UserCreate):
    if not user.name.strip():
        raise HTTPException(status_code=400, detail="Name darf nicht leer sein.")
    email_error = validateEmail(user.email)
    if email_error:
        raise HTTPException(status_code=400, detail=email_error)
    pw_error = validatePassword(user.password)
    if pw_error:
        raise HTTPException(status_code=400, detail=pw_error)

    konto = createKonto(
        email=user.email,
        name=user.name,
        hashed_password=hashPassword(user.password),
    )
    if konto is None:
        raise HTTPException(status_code=400, detail="E-Mail bereits registriert")

    return User(email=konto["email"], name=konto["name"])


@router.post("/auth/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    konto = getKontoByEmail(form_data.username)
    if not konto or not verifyPassword(form_data.password, konto["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-Mail oder Passwort falsch",
        )
    return createTokenPair(konto)


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

    # Konto-Daten für neues Token-Paar zusammenstellen
    konto = {"id": entry["konto_id"], "email": entry["email"]}
    return createTokenPair(konto)


@router.post("/auth/logout")
async def logout(body: LogoutRequest):
    """Löscht den Refresh Token serverseitig → Token wird ungültig."""
    deleteRefreshToken(body.refresh_token)
    return {"detail": "Erfolgreich abgemeldet"}


# ── Geschützte Endpunkte ───────────────────────────────────────

@router.get("/users/me", response_model=User)
async def readCurrentUser(current_user: Annotated[User, Depends(getCurrentUser)]):
    """Nur mit gültigem Access Token erreichbar."""
    return current_user


@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
async def deleteCurrentUser(current_user: Annotated[User, Depends(getCurrentUser)]):
    """Löscht das eigene Konto inkl. aller Refresh Tokens (CASCADE)."""
    deleteKonto(current_user.email)