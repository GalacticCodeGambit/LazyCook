from typing import Dict, Any


class Datenbank:
    def __init__(self):
        pass

    def verbindeDB(self):
        pass

    def speichernInDB(self, daten: Dict[str, Any]):
        pass

    def holeDaten(self, tabelle: str) -> list[Dict[str, Any]]:
        pass
