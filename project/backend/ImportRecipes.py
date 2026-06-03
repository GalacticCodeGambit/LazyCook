import json
from Recipe import Recipe
from Ingredient import Ingredient
from Database import getAllIngredients, getAllRecipes
from pathlib import Path

EXCLUDE_INGREDIENTS = ["Salz", "Pfeffer", "Zucker"]
PATH = Path(__file__).parent.parent /"recipes_perfect.json"

def extractRecipesFromJSON(filePath: str) -> list[Recipe]:
    recipesRaw = json.loads(__readJsonFile(filePath=filePath))
    recipes = []
    for recipeData in recipesRaw:
        recipe = __formatRecipe(
            recipeData["Name"],
            recipeData["Ingredients"],
            recipeData["Instructions"]
        )
        __saveRecipeInDB(recipe)
        recipes.append(recipe)
    return recipes

def __readJsonFile(filePath: str) -> str:
    # Hier encoding="utf-8" hinzufügen!
    with open(filePath, "r", encoding="utf-8") as file:
        return file.read()

def __formatRecipe(name: str,ingredientsRaw: dict, description: str)-> Recipe:
    ingredients = []
    for ingredient in ingredientsRaw:
        formattedIngredient = __formatIngredient(ingredient)
        if formattedIngredient:
            ingredients.append(formattedIngredient)
    recipe = Recipe(name, ingredients, description)
    return recipe

def __formatIngredient(rawText: str) -> Ingredient:
    for exclude in EXCLUDE_INGREDIENTS:
        if exclude in rawText:
            return None
    amount, amountType, name = __formatIngredientText(rawText)
    if not name:
        return None
    ingredient = Ingredient(name, amount)
    ingredient.setAmountType(amountType)
    __saveIngridientInDB(ingredient)
    return ingredient

def __formatIngredientText(rawText: str) -> str:
    rawText = rawText.replace(",", "")
    sliced = rawText.split(" ")
    if len(sliced) < 2:
        return None, None, None
    elif sliced[0].isnumeric():
        amount = float(sliced[0])
        amountType = sliced[1]
        name = " ".join(sliced[2:])
    else:
        amount = 1
        amountType = ""
        name = rawText
    return amount, amountType, name

def __saveIngridientInDB(ingredient: Ingredient) -> bool:
    for ingredients in getAllIngredients():
        if ingredient.getName() == ingredients["name"]:
            return False
    return ingredient.saveInDB()

def __saveRecipeInDB(recipe: Recipe):
    for recipes in getAllRecipes():
        if recipe.getName().lower().strip() == recipes["name"].lower().strip():
            return False
    return recipe.saveInDB()
        

if __name__ == "__main__":
    recipes = extractRecipesFromJSON(str(PATH))
    for r in recipes:
        print(r.getName())