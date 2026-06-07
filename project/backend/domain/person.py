class Person:
    def __init__(self, name: str, email: str, password: str):
        self.__name = name
        self.__email = email
        self.__password = password
        self.__role = "User"

    def getName(self) -> str:
        return self.__name

    def setName(self, name: str):
        self.__name = name

    def getEmail(self) -> str:
        return self.__email

    def setEmail(self, email: str):
        self.__email = email

    def getPassword(self) -> str:
        return self.__password

    def setPassword(self, password: str):
        self.__password = password

    def getRole(self) -> str:
        return self.__role

    def setRole(self, role: str):
        self.__role = role
