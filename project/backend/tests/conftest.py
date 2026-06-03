import os

# Setzt den JWT-Secret vor dem Import von core.Auth,
# damit der Modul-Level-Check nicht fehlschlägt.
# Wird nur verwendet wenn die Variable noch nicht gesetzt ist (z.B. lokal oder in CI ohne Docker).
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-ci-only")
