from Database import getAllRecipes

def getMatchingRecipeNames(searchTerm: str) -> list[str]:
    """Gibt eine Liste von Rezeptnamen zurück, die den Suchbegriff enthalten."""
    searchTerm = searchTerm.lower()
    matchingRecipes = []
    for recipe in getAllRecipes():
        if searchTerm in recipe["name"].lower():
            matchingRecipes.append(recipe["name"])
    return matchingRecipes