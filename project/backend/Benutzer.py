from project.backend.Person import Person
from project.backend.Rezept import Rezept


class Benutzer(Person):
    def __init__(self, name: str, email: str, passwort: str):
        super().__init__(name, email, passwort)
        super().setRole("User")

