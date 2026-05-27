from typing import List, Dict, Any
from Database import addIngredient, getAllIngredientsForRecipe


class Ingredient:
    def __init__(self, name: str, amount: float):
        self.__name = name
        self.__amount = amount
        self.__amountType = None

    def getName(self) -> str:
        return self.__name

    def setName(self, name: str):
        self.__name = name

    def getAmount(self) -> float:
        return self.__amount

    def setAmount(self, amount: float):
        self.__amount = amount

    def setAmountType(self, amountType: str):
        self.__amountType = amountType

    def getAmountType(self):
        return self.__amountType

    def saveInDB(self) -> bool:
        if not self.__amountType:
            return False
        else:
            zid = addIngredient(self.__name, self.__amountType)
            if not zid:
                return False
            else:
                return True

    def formatIngredients(id: int) -> list[Ingredient]:
        IngredientsRaw = getAllIngredientsForRecipe(id)
        Ingredients = []
        for IngredientRaw in IngredientsRaw:
            Ingredients.append(
                Ingredient(IngredientRaw["name"], IngredientRaw["amount"])
            )
        return Ingredients
