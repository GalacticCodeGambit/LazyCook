import json
from domain.recipe import Recipe
from domain.ingredient import Ingredient
from dao import IngredientDAO, RecipeDAO
from pathlib import Path

EXCLUDE_INGREDIENTS = ["Salz", "Pfeffer", "Zucker"]
PATH = Path(__file__).parent.parent / "ImportRecipes" / "recipes_metric.json"


def extractRecipesFromJSON(filePath: str) -> list[Recipe]:
    recipesRaw = json.loads(__readJsonFile(filePath=filePath))
    recipes = []
    for recipeData in recipesRaw:
        recipe = __formatRecipe(
            recipeData["Name"],
            recipeData["Ingredients"],
            "", # recplace with Instructions, as soon as json complete
        )
        __saveRecipeInDB(recipe)
        recipes.append(recipe)
    return recipes


def __readJsonFile(filePath: str) -> str:
    with open(filePath, "r", encoding="utf-8") as file:
        return file.read()


def __formatRecipe(name: str, ingredientsRaw: dict, description: str) -> Recipe:
    ingredients = []
    for ingredient in ingredientsRaw:
        formattedIngredient = __formatIngredient(ingredient)
        if formattedIngredient:
            ingredients.append(formattedIngredient)
    return Recipe(name, ingredients, description)


def __formatIngredient(rawText: str) -> Ingredient | None:
    for exclude in EXCLUDE_INGREDIENTS:
        if exclude in rawText:
            return None
    amount, amountType, name = __formatIngredientText(rawText)
    if not name:
        return None
    ingredient = Ingredient(name, amount)
    ingredient.setAmountType(amountType)
    __saveIngredientInDB(ingredient)
    return ingredient


def __formatIngredientText(rawText: str) -> tuple:
    rawText = rawText.replace(",", "")
    sliced = rawText.split(" ")
    if len(sliced) < 2:
        return None, None, None
    elif sliced[0].isnumeric():
        return float(sliced[0]), sliced[1], " ".join(sliced[2:])
    else:
        return 1, "", rawText


def __saveIngredientInDB(ingredient: Ingredient) -> bool:
    if IngredientDAO.getIngredientByName(ingredient.getName()):
        return False
    if not ingredient.getAmountType():
        return False
    IngredientDAO.addIngredient(ingredient.getName(), ingredient.getAmountType())
    return True


def __saveRecipeInDB(recipe: Recipe) -> bool:
    for existing in RecipeDAO.getAllRecipes():
        if recipe.getName().lower().strip() == existing["name"].lower().strip():
            return False
    rid = RecipeDAO.addRecipe(recipe.getName(), recipe.getDescription(), None)
    for ingredient in recipe.getIngredients():
        result = IngredientDAO.getIngredientByName(ingredient.getName())
        if result:
            RecipeDAO.addIngredientToRecipe(rid ,result["id"] ,ingredient.getAmount())
    return True


if __name__ == "__main__":
    recipes = extractRecipesFromJSON(str(PATH))
    for r in recipes:
        print(r.getName())
