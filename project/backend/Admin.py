from project.backend.Person import Person
from project.backend.Recipe import Recipe


class Admin(Person):
    def __init__(self, name: str, email: str, password: str):
        super().__init__(name, email, password)
        self.__ricepes = []
        super().setRole("Admin")

    def addRecipe(self, recipe: Recipe):
        self.__ricepes.append(recipe)
        