"""
routes/users.py – Geschützte User-Endpunkte (/users/me)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from core.Auth import getCurrentUser
from dao import AccountDAO
from services import UserService
from core.Models import User, UpdateUser

router = APIRouter()


@router.get("/users/me", response_model=User)
async def readCurrentUser(currentUser: Annotated[User, Depends(getCurrentUser)]):
    """Gibt die Daten des aktuell eingeloggten Users zurück."""
    return currentUser


@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
async def deleteCurrentUser(currentUser: Annotated[User, Depends(getCurrentUser)]):
    """Löscht das eigene Konto inkl. aller Refresh Tokens (CASCADE)."""
    AccountDAO.deleteAccount(currentUser.email)


@router.patch("/users/me")
async def updateCurrentUser(
    data: UpdateUser,
    currentUser: Annotated[User, Depends(getCurrentUser)],
):
    account = AccountDAO.getAccountByEmail(currentUser.email)
    try:
        UserService.updateUser(account["id"], account["email"], data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"success": True}
