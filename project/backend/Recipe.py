from project.backend.Database import Database
from project.backend.Ingridient import Ingridient


class Recipe:
    def __init__(self, name: str, ingridients: list[Ingridient], description: str):
        self.__name = name
        self.__Ingridienten = ingridients
        self.__description = description
        self.__original = ""
        self.__duration = ""
        self.__rating = 0
        self.__countPersons = 1
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

    def getRating(self) -> int:
        return self.rating

    def setRating(self, rating: int):
        self.rating = rating

    def getDuration(self) -> str:
        return self.duration

    def setDuration(self, duration: str):
        self.duration = duration

    def getIngridient(self) -> list[Ingridient]:
        return self.ingridients

    def setIngridient(self, ingridients: list[Ingridient]):
        self.ingridients = ingridients

