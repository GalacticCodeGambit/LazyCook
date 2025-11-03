from Project.Backend.Benutzer import Benutzer
from Project.Backend.Datenbank import Datenbank
from Project.Backend.Person import Person


class LazyCookVerwaltung:
    def __init__(self):
        self.__datenbank = Datenbank()
        self.__user = Person()

    def anmelden(self, email: str, passwort: str) -> bool:
        pass


    def registrieren(self, name: str, email: str, passwort: str):
        pass

    def filternNachZutat(self, anzPersonen: int, zutaten_liste: list[str]):
        pass

    def suchenNachRezept(self, name: str):
       pass

    def zeigeRezepteAn(self):
       pass