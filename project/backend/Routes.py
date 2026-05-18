import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from EmailService import sendPasswordChangedEmail, sendPasswordResetEmail


from Auth import (
    createTokenPair,
    getCurrentUser,
    hashPassword,
    validateEmail,
    validatePassword,
    validateRefreshToken,
    verifyPassword,
    createPasswordResetToken,
    validatePasswordResetToken,
)
from Database import (
    createAccount,
    getAccountByEmail,
    getAccountById,
    deleteRefreshToken,
    deleteAllRefreshTokens,
    deleteAccount,
    updateAccount,
    markResetTokenUsed,
    updateKontoPassword,
    incrementIngredientUsage,
    getTopIngredients,
)

from Models import (
    User,
    Token,
    UserCreate,
    RefreshRequest,
    LogoutRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    UpdateUser,
    RecipeSearchRequest,
)

# Frontend-URL aus Env, mit Dev-Fallback (Frontend läuft per compose.yaml auf Port 8000)
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:8000")

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
    Account = {"id": entry["AccountID"], "email": entry["email"]}
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



@router.patch("/users/me")
async def updateCurrentUser(
    data: UpdateUser, currentUser: Annotated[User, Depends(getCurrentUser)]
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


# ── Rezept-Endpunkte ───────────────────────────────────────────

# ------------ Passwort vergessen ----------------- #


@router.post("/auth/forgot-password")
async def forgotPassword(body: ForgotPasswordRequest):
    """Schritt 1: User gibt E-Mail ein, bekommt Reset-Link per Mail."""
    konto = getAccountByEmail(body.email)

    # Token nur erzeugen wenn Konto existiert – aber IMMER gleiche Antwort senden!
    if konto is not None:
        token = createPasswordResetToken(konto["id"])
        resetLink = f"{FRONTEND_URL}/reset-password?token={token}"
        try:
            sendPasswordResetEmail(body.email, konto["name"], resetLink)
        except Exception as e:
            # Mail-Fehler darf das Response nicht beeinflussen → User-Enumeration vermeiden
            print(f"Reset-Mail konnte nicht gesendet werden: {e}")

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

    updateKontoPassword(entry["kontoID"], hashPassword(body.new_password))
    markResetTokenUsed(entry["id"])
    # Sicherheitsmaßnahme: Alle aktiven Sessions ungültig machen
    deleteAllRefreshTokens(entry["kontoID"])

    # Bestätigungsmail an den Konto-Inhaber
    konto = getAccountById(entry["kontoID"])
    if konto is not None:
        try:
            sendPasswordChangedEmail(konto["email"], konto["name"])
        except Exception as e:
            print(f"Bestätigungsmail konnte nicht gesendet werden: {e}")

    return {"detail": "Passwort erfolgreich zurückgesetzt."}


# ── Recipe-Suche ───────────────────────────────────────────────


@router.post("/recipes/search")
async def searchRecipes(
    body: RecipeSearchRequest,
    currentUser: Annotated[User, Depends(getCurrentUser)],
):
    """Sucht Rezepte basierend auf den übergebenen Zutaten.

    Hinweis: Aktuell nur Usage-Tracking implementiert – die eigentliche
    Rezept-Suche folgt. Jede gesuchte Zutat erhöht den persönlichen Counter
    des Users (IngredientUsage), damit später die Top-5-Vorschläge daraus
    abgeleitet werden können.
    """
    Account = getAccountByEmail(currentUser.email)
    if Account is None:
        raise HTTPException(status_code=404, detail="Account nicht gefunden")

    # Usage-Tracking: jede gesuchte Zutat hochzählen (Hybrid: count + lastUsedAt + lastUnit)
    for zutat in body.zutaten:
        incrementIngredientUsage(Account["id"], zutat.name, zutat.unit)

    # Aktualisierte Top 5 direkt mit zurückgeben → Frontend muss keinen Extra-Request machen
    topRows = getTopIngredients(Account["id"], limit=5)
    topIngredients = [
        {"name": r["displayName"], "unit": r["lastUnit"]} for r in topRows
    ]

    # TODO: eigentliche Rezept-Suche implementieren
    return {"rezepte": [], "topIngredients": topIngredients}


# ── Ingredient-Vorschläge ──────────────────────────────────────


@router.get("/ingredients/top")
async def getTopIngredientsForUser(
    response: Response,
    currentUser: Annotated[User, Depends(getCurrentUser)],
    limit: int = 5,
):
    """Liefert die meistgenutzten Zutaten des aktuellen Users für die Vorschlags-Badges."""
    Account = getAccountByEmail(currentUser.email)
    if Account is None:
        raise HTTPException(status_code=404, detail="Account nicht gefunden")

    # Caching unterbinden – die Liste ändert sich mit jeder Suche
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"

    rows = getTopIngredients(Account["id"], limit=limit)
    return {
        "ingredients": [{"name": r["displayName"], "unit": r["lastUnit"]} for r in rows]
    }
