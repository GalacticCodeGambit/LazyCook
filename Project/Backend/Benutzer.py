from Project.Backend.Person import Person
from Project.Backend.Rezept import Rezept


class Benutzer(Person):
    def __init__(self, name: str, email: str, passwort: str):
        super().__init__(name, email, passwort)
        super().setRole("User")

