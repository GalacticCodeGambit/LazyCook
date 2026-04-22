from project.backend.Person import Person
from project.backend.Recipe import Recipe


class User(Person):
    def __init__(self, name: str, email: str, password: str):
        super().__init__(name, email, password)
        super().setRole("User")

