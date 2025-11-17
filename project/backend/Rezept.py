from project.backend.Datenbank import Datenbank
from project.backend.Zutat import Zutat


class Rezept:
    def __init__(self, name: str, zutaten: list[Zutat], zubereitung: str):
        self.__name = name
        self.__zutaten = zutaten
        self.__zubereitung = zubereitung
        self.__original = ""
        self.__dauer = ""
        self.__bewertung = 0
        self.__anzPersonen = 1
        self.__datenbank = Datenbank()

    def speichernInDB(self) -> bool:
        return True

    def getName(self) -> str:
        return self.name

    def setName(self, name: str):
        self.name = name

    def getOriginal(self) -> str:
        return self.original

    def setOriginal(self, original: str):
        self.original = original

    def getZubereitung(self) -> str:
        return self.zubereitung

    def setZubereitung(self, zubereitung: str):
        self.zubereitung = zubereitung

    def getBewertung(self) -> int:
        return self.bewertung

    def setBewertung(self, bewertung: int):
        self.bewertung = bewertung

    def getDauer(self) -> str:
        return self.dauer

    def setDauer(self, dauer: str):
        self.dauer = dauer

    def getZutaten(self) -> list[Zutat]:
        return self.zutaten

    def setZutaten(self, zutaten: list[Zutat]):
        self.zutaten = zutaten

