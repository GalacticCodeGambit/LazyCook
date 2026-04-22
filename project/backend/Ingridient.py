from typing import List, Dict, Any

class Ingridient:
    def __init__(self, name: str, quantity: float):
        self.__name = name
        self.__quantity = quantity

    def getName(self) -> str:
        return self.__name

    def setName(self, name: str):
        self.__name = name

    def getquantity(self) -> float:
        return self.__quantity

    def setquantity(self, quantity: float):
        self.__quantity = quantity

