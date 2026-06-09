"""
recipe_service.py – Geschäftslogik für Rezeptsuche
SUCUK = Search for Uncomplicated Cooking and User-friendly Kitchen recipes
"""

from domain.recipe import Recipe
from domain.ingredient import Ingredient
from core.Database import getDB


def findRecipes(ingredients: list, index: int) -> list[Recipe]:
    """Sucht Rezepte anhand einer Zutatenliste, sortiert nach Übereinstimmung (paginiert)."""
    if not ingredients:
        return _getAllRecipesPaginated(index)

    ingredientNames = [i.getName().lower() for i in ingredients]
    return _searchByIngredients(ingredientNames, index)


def _getAllRecipesPaginated(index: int) -> list[Recipe]:
    """Gibt alle Rezepte paginiert zurück ohne Scoring."""
    offset = 12 * index
    with getDB() as con:
        cur = con.cursor()
        cur.execute("""
                    SELECT r.id, r.name, r.description
                    FROM Recipe r
                    ORDER BY r.name
                        LIMIT 12 OFFSET ?
                    """, (offset,))
        rows = cur.fetchall()

    recipes = []
    for row in rows:
        ingredients = _getIngredients(row["id"])
        recipe = Recipe(row["name"], ingredients, row["description"] or "")
        recipes.append(recipe)
    return recipes


def _searchByIngredients(ingredientNames: list[str], index: int) -> list[Recipe]:
    offset = 12 * index

    # LIKE-Bedingungen für jeden Suchbegriff
    likeConditions = " OR ".join(
        ["LOWER(i.name) LIKE ?"] * len(ingredientNames)
    )
    likeParams = [f"%{name}%" for name in ingredientNames]

    with getDB() as con:
        cur = con.cursor()
        cur.execute(f"""
            SELECT
                r.id,
                r.name,
                r.description,
                COUNT(DISTINCT CASE
                    WHEN {likeConditions} THEN i.id
                END) AS matching,
                COUNT(DISTINCT ef.zid) AS total
            FROM Recipe r
            LEFT JOIN Exists_from ef ON ef.rid = r.id
            LEFT JOIN Ingredient i ON i.id = ef.zid
            GROUP BY r.id
            ORDER BY matching DESC, r.name
            LIMIT 12 OFFSET ?
        """, (*likeParams, offset))
        rows = cur.fetchall()

    recipes = []
    for row in rows:
        ingredientObjs = _getIngredients(row["id"])
        recipe = Recipe(row["name"], ingredientObjs, row["description"] or "")
        matching = row["matching"] or 0
        total = row["total"] or 1
        recipe.setRating(matching / total if total > 0 else 0)
        for _ in range(matching):
            recipe.incrementMatching()
        recipes.append(recipe)
    return recipes

def _getIngredients(recipeId: int) -> list[Ingredient]:
    """Lädt die Zutaten eines einzelnen Rezepts."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("""
                    SELECT i.name, ef.amount
                    FROM Ingredient i
                             JOIN Exists_from ef ON i.id = ef.zid
                    WHERE ef.rid = ?
                    """, (recipeId,))
        return [Ingredient(row["name"], row["amount"]) for row in cur.fetchall()]