from Person import Person
from Recipe import Recipe


class User(Person):
    def __init__(self, name: str, email: str, password: str):
        super().__init__(name, email, password)
        super().setRole("User")
