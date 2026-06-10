import os

# Setzt den JWT-Secret vor dem Import von core.Auth, damit der Modul-Level-Check
# nicht fehlschlaegt. Ein leerer Wert (z.B. fehlendes CI-Secret -> "") wird wie
# "nicht gesetzt" behandelt, da os.environ.setdefault einen vorhandenen leeren
# String nicht ueberschreiben wuerde.
if not os.environ.get("JWT_SECRET_KEY"):
    os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-ci-only"
