from Database import getAllRecipes
from Ingredient import Ingredient
from Recipe import Recipe


def getMatchingRecipeNames(searchTerm: str) -> list[Recipe]:
    """Gibt eine Liste von Rezepten zurück, die den Suchbegriff enthalten."""
    searchTerm = searchTerm.lower()
    matchingRecipes = []
    for recipe in getAllRecipes():
        if searchTerm in recipe["name"].lower():
            matchingRecipes.append(
                Recipe(
                    recipe["name"],
                    Ingredient.formatIngredients(recipe["id"]),
                    recipe["description"],
                )
            )
    return matchingRecipes
