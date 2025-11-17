from typing import List, Dict, Any

class Zutat:
    def __init__(self, name: str, menge: float):
        self.__name = name
        self.__menge = menge

    def getName(self) -> str:
        return self.__name

    def setName(self, name: str):
        self.__name = name

    def getMenge(self) -> float:
        return self.__menge

    def setMenge(self, menge: float):
        self.__menge = menge

