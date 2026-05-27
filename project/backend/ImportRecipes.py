from Recipe import Recipe
from Ingredient import Ingredient
from Database import getAllIngredients

EXCLUDE_INGREDIENTS = ["Salz", "Pfeffer", "Zucker"]

def extractRecipesFromJSON():
    pass

def __formatRecipe(name: str,ingredientsRaw: dict, description: str)-> Recipe:
    ingredients = []
    for ingredient in ingredientsRaw:
        formattedIngredient = __formatIngredient(ingredient)
        if formattedIngredient:
            ingredients.append(formattedIngredient)
    recipe = Recipe(name, ingredients, description)
    recipe.saveInDB()
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




