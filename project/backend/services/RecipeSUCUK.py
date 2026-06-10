"""
recipe_service.py – Geschäftslogik für Rezeptsuche
SUCUK = Search for Uncomplicated Cooking and User-friendly Kitchen recipes
"""

from domain.recipe import Recipe
from domain.ingredient import Ingredient
from dao import IngredientDAO, RecipeDAO


def findRecipes(ingredients: list, index: int) -> list[Recipe]:
    """Sucht Rezepte anhand einer Zutatenliste, sortiert nach Übereinstimmung (paginiert)."""
    recipes = _initRecipes()

    for ingredient in ingredients:
        _scoreRecipes(recipes, ingredient)

    recipes.sort(key=lambda r: r.getRating(), reverse=True)
    return recipes[12 * index : 12 * (index + 1)]


def getMatchingRecipeNames(searchTerm: str) -> list[Recipe]:
    """Gibt Rezepte zurück, deren Name den Suchbegriff enthält."""
    searchTerm = searchTerm.lower()
    return [
        Recipe(
            r["name"], IngredientDAO.getIngredientsForRecipe(r["id"]), r["description"]
        )
        for r in RecipeDAO.getAllRecipes()
        if searchTerm in r["name"].lower()
    ]


def _initRecipes() -> list[Recipe]:
    rows = RecipeDAO.getAllRecipesWithIngredients()
    result = []
    for r in rows:
        ingredients = []
        for i in r["ingredients"]:
            ing = Ingredient(i["name"], i["amount"])
            ing.setAmountType(i["amountType"])
            ingredients.append(ing)
        result.append(Recipe(r["name"], ingredients, r["description"] or ""))
    return result


def _scoreRecipes(recipes: list[Recipe], ingredient) -> None:
    for recipe in recipes:
        for recipeIngredient in recipe.getIngredients():
            if ingredient.getName() in recipeIngredient.getName():
                recipe.incrementMatching()
                recipe.setRating(recipe.getMatching() / len(recipe.getIngredients()))
