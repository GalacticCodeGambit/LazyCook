class Ingredient:
    def __init__(self, name: str, amount: float):
        self.__name = name
        self.__amount = amount
        self.__amountType = None

    def getName(self) -> str:
        return self.__name

    def setName(self, name: str):
        self.__name = name

    def getAmount(self) -> float:
        return self.__amount

    def setAmount(self, amount: float):
        self.__amount = amount

    def setAmountType(self, amountType: str):
        self.__amountType = amountType

    def getAmountType(self):
        return self.__amountType
