from Project.backend.Person import Person
from Project.backend.Rezept import Rezept


class Admin(Person):
    def __init__(self, name: str, email: str, passwort: str):
        super().__init__(name, email, passwort)
        self.__rezepte = []
        super().setRole("Admin")

    def fuegeRezeptHinzu(self, rezept: Rezept):
        self.__rezepte.append(rezept)
        print(f"Rezept '{rezept.getName()}' wurde zu Benutzer '{self.name}' hinzugefügt.")
