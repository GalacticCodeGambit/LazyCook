"""
routes/recipes.py – Rezept- und Zutaten-Endpunkte
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response

from core.Auth import getCurrentUser
from dao import AccountDAO, IngredientDAO
from core.Models import User, RecipeSearchRequest
from domain.ingredient import Ingredient
from services.RecipeSUCUK import findRecipes

router = APIRouter()


@router.post("/recipes/search")
async def searchRecipes(
        body: RecipeSearchRequest,
        currentUser: Annotated[User, Depends(getCurrentUser)],
):
    account = AccountDAO.getAccountByEmail(currentUser.email)
    if account is None:
        raise HTTPException(status_code=404, detail="Account nicht gefunden")

    for zutat in body.zutaten:
        IngredientDAO.incrementIngredientUsage(account["id"], zutat.name, zutat.unit)

    # Echte Rezept-Suche
    ingredients = [Ingredient(z.name, z.amount) for z in body.zutaten]
    index = getattr(body, "index", 0)
    recipes = findRecipes(ingredients, index)

    topRows = IngredientDAO.getTopIngredients(account["id"], limit=5)
    topIngredients = [
        {"name": r["displayName"], "unit": r["lastUnit"]} for r in topRows
    ]

    return {
        "rezepte": [
            {
                "name": r.getName(),
                "description": r.getDescription(),
                "rating": r.getRating(),
                "duration": r.getDuration() if hasattr(r, "getDuration") else "",
                "matching": r.getMatching(),
                "ingredients": [
                    {"name": i.getName(), "amount": i.getAmount()}
                    for i in r.getIngredients()
                ]
            }
            for r in recipes
        ],
        "topIngredients": topIngredients
    }


@router.get("/ingredients/top")
async def getTopIngredientsForUser(
        response: Response,
        currentUser: Annotated[User, Depends(getCurrentUser)],
        limit: int = 5,
):
    account = AccountDAO.getAccountByEmail(currentUser.email)
    if account is None:
        raise HTTPException(status_code=404, detail="Account nicht gefunden")

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"

    rows = IngredientDAO.getTopIngredients(account["id"], limit=limit)
    return {
        "ingredients": [{"name": r["displayName"], "unit": r["lastUnit"]} for r in rows]
    }