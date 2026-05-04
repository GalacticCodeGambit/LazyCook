from Database import Database
from Ingridient import Ingridient


class Recipe:
    def __init__(self, name: str, ingridients: list[Ingridient], description: str):
        self.__name = name
        self.__Ingridients = ingridients
        self.__description = description
        self.__original = ""
        self.__duration = ""
        self.__rating = 0.0
        self.__countPersons = 1
        self.__matching = 0
        self.__database = Database()

    def saveInDB(self) -> bool:
        return True

    def getName(self) -> str:
        return self.name

    def setName(self, name: str):
        self.name = name

    def getOriginal(self) -> str:
        return self.original

    def setOriginal(self, original: str):
        self.original = original

    def getDescription(self) -> str:
        return self.description

    def setDescription(self, description: str):
        self.description = description

    def getRating(self) -> float:
        return self.__rating

    def setRating(self, rating: float):
        self.__rating = rating

    def getMatching(self) -> int:
        return self.__matching

    def incrementMatching(self):
        self.__matching+=1

    def getDuration(self) -> str:
        return self.duration

    def setDuration(self, duration: str):
        self.duration = duration

    def getIngridients(self) -> list[Ingridient]:
        return self.__ingridients

    def setIngridient(self, ingridients: list[Ingridient]):
        self.__Ingridients = ingridients

