from Database import getAllRecipes, getAllIngredientsForRecipe
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
                    __formatIngredients(recipe["id"]),
                    recipe["description"],
                )
            )
    return matchingRecipes


def __formatIngredients(id: int) -> list[Ingredient]:
    IngredientsRaw = getAllIngredientsForRecipe(id)
    Ingredients = []
    for IngredientRaw in IngredientsRaw:
        Ingredients.append(Ingredient(IngredientRaw["name"], IngredientRaw["amount"]))
    return Ingredients
