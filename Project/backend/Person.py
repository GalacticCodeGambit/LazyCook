class Person:
    def __init__(self, name: str, email: str, passwort: str):
        self.__name = name
        self.__email = email
        self.__passwort = passwort
        self.__role = "User"

    def speichernInDB(self) -> bool:
        return True

    def getName(self) -> str:
        return self.__name

    def setName(self, name: str):
        self.__name = name

    def getEmail(self) -> str:
        return self.__email

    def setEmail(self, email: str):
        self.__email = email

    def getPasswort(self) -> str:
        return self.__passwort

    def setPasswort(self, passwort: str):
        self.__passwort = passwort

    def getRole(self) -> str:
        return self.__role

    def setRole(self, role: str):
        self.__role = role