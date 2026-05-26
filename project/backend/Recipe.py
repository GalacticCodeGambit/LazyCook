from Ingredient import Ingredient
from Database import addIngredientToRecipe, addRecipe, getIngridientByName


class Recipe:
    def __init__(self, name: str, ingredients: list[Ingredient], description: str):
        self.__name = name
        self.__ingredients = ingredients
        self.__description = description
        self.__original = ""
        self.__duration = ""
        self.__rating = 0.0
        self.__countPersons = 1
        self.__matching = 0

    def saveInDB(self) -> bool:
        rid = addRecipe(self.__name, self.__description, None)
        for ingridient in self.__ingredients:
            zid = getIngridientByName(ingridient.getName())['id']
            if not zid:
                return False
            else:
                addIngredientToRecipe(zid, rid, ingridient.getAmount())
        return True

    def getName(self) -> str:
        return self.__name

    def setName(self, name: str):
        self.__name = name

    def getOriginal(self) -> str:
        return self.__original

    def setOriginal(self, original: str):
        self.__original = original

    def getDescription(self) -> str:
        return self.__description

    def setDescription(self, description: str):
        self.__description = description

    def getRating(self) -> float:
        return self.__rating

    def setRating(self, rating: float):
        self.__rating = rating

    def getMatching(self) -> int:
        return self.__matching

    def incrementMatching(self):
        self.__matching += 1

    def getDuration(self) -> str:
        return self.__duration

    def setDuration(self, duration: str):
        self.__duration = duration

    def getIngredients(self) -> list[Ingredient]:
        return self.__ingredients

    def setIngredient(self, ingredients: list[Ingredient]):
        self.__ingredients = ingredients
