from typing import List, Dict, Any


class Ingredient:
    def __init__(self, name: str, amount: float):
        self.__name = name
        self.__amount = amount

    def getName(self) -> str:
        return self.__name

    def setName(self, name: str):
        self.__name = name

    def getAmount(self) -> float:
        return self.__amount

    def setAmount(self, amount: float):
        self.__amount = amount
