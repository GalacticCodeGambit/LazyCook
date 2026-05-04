import Database
from Ingridient import Ingridient
from Recipe import Recipe
from Database import  getAllRecipes, getAllIngridientsForRecipe

def findRecipes(ingriedents: list[Ingridient])-> list[Recipe]:
    recipes = __initRecipes()
 
    for ingridient in ingriedents:
        recipes = __filterRecipes(recipes)

    recipes.sort(key=lambda x: x.getRating(), reverse=True)
    
    for recipe in recipes[::-1]:
        if recipe.getMatching < 3:
            recipes.remove(recipe)
        else:
            break
    return recipes

def __filterRecipes(recipes: list[Recipe], ingridient: Ingridient)-> list[Recipe]:
    for recipe in recipes:
        for recipeIngridient in recipe.getIngridients():
            if recipeIngridient.getName() == ingridient.getName():
                recipe.incrementMatching()
                recipe.setRating(recipe.getMatching/ len(recipe.getIngridients))                
    return recipes

def __initRecipes()-> list[Recipe]:
    recipesRaw = getAllRecipes
    recipes = []
    for recipeRaw in recipesRaw:
        recipe = Recipe(recipeRaw["name"], __formatIngridients(recipeRaw["id"]), recipeRaw["description"])
        recipes.append(recipe)
    return recipes

def __formatIngridients(id: int)-> list[Ingridient]:
    ingridientsRaw = getAllIngridientsForRecipe(id)
    ingridients = []
    for ingridientRaw in ingridientsRaw:
        ingridients.append(Ingridient(ingridientRaw["name"],ingridientRaw["amount"]))
    return ingridients