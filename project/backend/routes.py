from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from EmailService import send_password_changed_email
from pydantic import BaseModel as _BaseModel


from auth import (
    Token,
    User,
    UserCreate,
    RefreshRequest,
    LogoutRequest,
    create_token_pair,
    get_current_user,
    hash_password,
    validate_email,
    validate_password,
    validate_refresh_token,
    verify_password,
    create_access_token,
)
from Datenbank import (
    create_konto,
    get_konto_by_email,
    delete_refresh_token,
    delete_all_refresh_tokens,
    delete_konto,
    update_konto,
)

router = APIRouter()


# ── Auth-Endpunkte ─────────────────────────────────────────────

@router.post("/auth/register", response_model=User)
async def register(user: UserCreate):
    if not user.name.strip():
        raise HTTPException(status_code=400, detail="Name darf nicht leer sein.")
    email_error = validate_email(user.email)
    if email_error:
        raise HTTPException(status_code=400, detail=email_error)
    pw_error = validate_password(user.password)
    if pw_error:
        raise HTTPException(status_code=400, detail=pw_error)

    konto = create_konto(
        email=user.email,
        name=user.name,
        hashed_password=hash_password(user.password),
    )
    if konto is None:
        raise HTTPException(status_code=400, detail="E-Mail bereits registriert")

    return User(email=konto["email"], name=konto["name"])


@router.post("/auth/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    konto = get_konto_by_email(form_data.username)
    if not konto or not verify_password(form_data.password, konto["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-Mail oder Passwort falsch",
        )
    return create_token_pair(konto)


@router.post("/auth/refresh", response_model=Token)
async def refresh(body: RefreshRequest):
    """Tauscht einen gültigen Refresh Token gegen ein neues Token-Paar."""
    entry = validate_refresh_token(body.refresh_token)
    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token ungültig oder abgelaufen",
        )

    # Alten Refresh Token löschen (Rotation – jeder Token ist nur einmal verwendbar)
    delete_refresh_token(body.refresh_token)

    # Konto-Daten für neues Token-Paar zusammenstellen
    konto = {"id": entry["konto_id"], "email": entry["email"]}
    return create_token_pair(konto)


@router.post("/auth/logout")
async def logout(body: LogoutRequest):
    """Löscht den Refresh Token serverseitig → Token wird ungültig."""
    delete_refresh_token(body.refresh_token)
    return {"detail": "Erfolgreich abgemeldet"}


# ── Geschützte Endpunkte ───────────────────────────────────────

@router.get("/users/me", response_model=User)
async def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    """Nur mit gültigem Access Token erreichbar."""
    return current_user


@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    """Löscht das eigene Konto inkl. aller Refresh Tokens (CASCADE)."""
    delete_konto(current_user.email)

    # ── Konto aktualisieren ────────────────────────────────────────

class UpdateUser(_BaseModel):
    email: str | None = None
    currentPassword: str | None = None
    newPassword: str | None = None

@router.patch("/users/me")
async def updateCurrentUser(
        data: UpdateUser,
        current_user: Annotated[User, Depends(get_current_user)]
):
    konto = get_konto_by_email(current_user.email)

    # E-Mail ändern
    if data.email:
        fehler = validate_email(data.email)
        if fehler:
            raise HTTPException(status_code=400, detail=fehler)
        update_konto(konto["id"], email=data.email)

    # Passwort ändern
    if data.currentPassword and data.newPassword:
        if not verify_password(data.currentPassword, konto["hashed_password"]):
            raise HTTPException(status_code=401, detail="Falsches Passwort")

        fehler = validate_password(data.newPassword)
        if fehler:
            raise HTTPException(status_code=400, detail=fehler)

        neuer_hash = hash_password(data.newPassword)
        update_konto(konto["id"], password_hash=neuer_hash)

        # NEU: try/catch um echten Fehler zu sehen
        empfaenger_email = data.email if data.email else konto["email"]
        try:
            send_password_changed_email(empfaenger_email, konto["name"])
        except Exception as e:
            print(f"E-Mail konnte nicht gesendet werden: {e}")

    return {"success": True}