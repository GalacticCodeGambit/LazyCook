# SUCUK = Search for Uncomplicated Cooking and User-friendly Kitchen recipes
from Ingredient import Ingredient
from Recipe import Recipe
from Database import getAllRecipes


def findRecipes(ingredients: list[Ingredient], index: int) -> list[Recipe]:
    recipes = __initRecipes()

    for ingredient in ingredients:
        recipes = __filterRecipes(recipes, ingredient)

    recipes.sort(key=lambda x: x.getRating(), reverse=True)

    return recipes[12*index:12*(index+1)]


def __filterRecipes(recipes: list[Recipe], ingredient: Ingredient) -> list[Recipe]:
    for recipe in recipes:
        for recipeIngredient in recipe.getIngredients():
            if recipeIngredient.getName() == ingredient.getName():
                recipe.incrementMatching()
                recipe.setRating(recipe.getMatching() / len(recipe.getIngredients()))
    return recipes


def __initRecipes() -> list[Recipe]:
    recipesRaw = getAllRecipes()
    recipes = []
    for recipeRaw in recipesRaw:
        recipe = Recipe(
            recipeRaw["name"],
            Ingredient.formatIngredients(recipeRaw["id"]),
            recipeRaw["description"],
        )
        recipes.append(recipe)
    return recipes


if __name__ == "__main__":
    ini = []
    ini.append(Ingredient("Linguine", 10))
    ini.append(Ingredient("Fresh Basil", 10))
    ini.append(Ingredient("Pine Nuts", 10))
    ini.append(Ingredient("Parmesan", 10))
    ini.append(Ingredient("Ground Beef", 10))
    ini.append(Ingredient("Cumin", 10))
    ini.append(Ingredient("Cucumber", 10))
    arr = findRecipes(ini)
    for i in arr:
        print(i.getName() + " " + str(i.getRating()))
