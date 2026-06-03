"""
routes/recipes.py – Rezept- und Zutaten-Endpunkte
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response

from core.Auth import getCurrentUser
from dao import AccountDAO, IngredientDAO
from core.Models import User, RecipeSearchRequest

router = APIRouter()


@router.post("/recipes/search")
async def searchRecipes(
    body: RecipeSearchRequest,
    currentUser: Annotated[User, Depends(getCurrentUser)],
):
    """Sucht Rezepte basierend auf den übergebenen Zutaten und trackt die Nutzung."""
    account = AccountDAO.getAccountByEmail(currentUser.email)
    if account is None:
        raise HTTPException(status_code=404, detail="Account nicht gefunden")

    for zutat in body.zutaten:
        IngredientDAO.incrementIngredientUsage(account["id"], zutat.name, zutat.unit)

    topRows = IngredientDAO.getTopIngredients(account["id"], limit=5)
    topIngredients = [
        {"name": r["displayName"], "unit": r["lastUnit"]} for r in topRows
    ]

    # TODO: eigentliche Rezept-Suche implementieren
    return {"rezepte": [], "topIngredients": topIngredients}


@router.get("/ingredients/top")
async def getTopIngredientsForUser(
    response: Response,
    currentUser: Annotated[User, Depends(getCurrentUser)],
    limit: int = 5,
):
    """Liefert die meistgenutzten Zutaten des aktuellen Users."""
    account = AccountDAO.getAccountByEmail(currentUser.email)
    if account is None:
        raise HTTPException(status_code=404, detail="Account nicht gefunden")

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"

    rows = IngredientDAO.getTopIngredients(account["id"], limit=limit)
    return {
        "ingredients": [{"name": r["displayName"], "unit": r["lastUnit"]} for r in rows]
    }
