# Code-Metriken Übersicht
### Duplikate · Testabdeckung · Zyklomatische Komplexität

---

## 1. Duplikate (Code Duplication)

### Was ist die Metrik?

Duplikate messen, wie oft identischer oder sehr ähnlicher Code an mehreren Stellen vorkommt. Tools wie SonarQube oder Lizard markieren Blöcke als dupliziert, wenn sie ab einer bestimmten Länge (z. B. 10 Zeilen) inhaltlich übereinstimmen.

**Ziel:** Jede Logik existiert genau einmal → Änderungen müssen nur an einer Stelle gemacht werden.

---

### Beispiel aus dem Projekt: `RecipeSUCUK.py`

Vor dem Refactoring gab es zwei fast identische List Comprehensions an zwei verschiedenen Stellen:

**Vor dem Refactoring (duplizierter Code):**

```python
# In findRecipes():
def _initRecipes() -> list[Recipe]:
    return [
        Recipe(r["name"], IngredientDAO.getIngredientsForRecipe(r["id"]), r["description"])
        for r in RecipeDAO.getAllRecipes()
    ]

# In getMatchingRecipeNames():
def getMatchingRecipeNames(searchTerm: str) -> list[Recipe]:
    searchTerm = searchTerm.lower()
    return [
        Recipe(r["name"], IngredientDAO.getIngredientsForRecipe(r["id"]), r["description"])
        for r in RecipeDAO.getAllRecipes()
        if searchTerm in r["name"].lower()
    ]
```

Der Kern – `Recipe(r["name"], IngredientDAO.getIngredientsForRecipe(r["id"]), r["description"])` –
ist in beiden Funktionen identisch. Das ist ein klassisches Duplikat.

**Nach dem Refactoring (Duplikat entfernt):**

```python
def _toRecipe(r: dict) -> Recipe:
    """Konvertiert eine Datenbankzeile in ein Recipe-Objekt."""
    return Recipe(r["name"], IngredientDAO.getIngredientsForRecipe(r["id"]), r["description"])

def _initRecipes() -> list[Recipe]:
    return [_toRecipe(r) for r in RecipeDAO.getAllRecipes()]

def getMatchingRecipeNames(searchTerm: str) -> list[Recipe]:
    searchTerm = searchTerm.lower()
    return [
        _toRecipe(r)
        for r in RecipeDAO.getAllRecipes()
        if searchTerm in r["name"].lower()
    ]
```

**Warum besser?** Wenn sich das `Recipe`-Objekt ändert (z. B. ein neues Pflichtfeld), muss nur `_toRecipe()` angepasst werden – nicht zwei Stellen.

---

### Wo ist eine schlechte Duplikat-Metrik akzeptabel?

In `AuthRoutes.py` wird die Validierungslogik in mehreren Endpunkten wiederholt:

```python
# In /auth/register:
emailError = validateEmail(user.email)
if emailError:
    raise HTTPException(status_code=400, detail=emailError)
pwError = validatePassword(user.password)
if pwError:
    raise HTTPException(status_code=400, detail=pwError)

# In /auth/reset-password:
pwError = validatePassword(body.new_password)
if pwError:
    raise HTTPException(status_code=400, detail=pwError)
```

Dieses Muster sieht dupliziert aus, ist aber **bewusst so** – jeder HTTP-Endpunkt muss seine eigenen Eingaben validieren. Eine Zusammenfassung würde die Route-Logik mit generischer Validierung vermischen und SRP verletzen. Das ist ein Fall, wo die Metrik "schlecht" ist, aber **kein Handlungsbedarf** besteht.

---

## 2. Testabdeckung (Code Coverage)

### Was ist die Metrik?

Coverage misst, welcher Prozentsatz der Codezeilen (Line Coverage) oder Verzweigungen (Branch Coverage) von automatisierten Tests ausgeführt wird. Ein Wert von 80 % bedeutet: 80 % der Zeilen werden beim Testlauf mindestens einmal durchlaufen.

**Ziel:** Möglichst viel Code ist durch Tests abgesichert, damit Fehler früh auffallen.

---

### Gutes Beispiel: `RecipeSUCUK.py` mit `test_recipe_sucuk.py`

`findRecipes()` hat eine hohe Coverage, weil die Tests systematisch alle Pfade abdecken:

```python
# Getestete Szenarien in test_recipe_sucuk.py:

class TestFindRecipesKeinTreffer:
    def testLeereDB(self):          # Pfad: leere Rezeptliste
    def testKeineUebereinstimmung() # Pfad: Zutaten vorhanden, aber kein Match
    def testLeereZutatenliste()     # Pfad: keine Suchzutaten übergeben

class TestFindRecipesTreffer:
    def testEinTreffer()            # Pfad: ein Rezept trifft zu
    def testMehrereTrefferSortiert()# Pfad: Sortierung nach Rating
    def testRatingBerechnung()      # Pfad: Rating-Formel korrekt
    def testAlleZutatenTreffen()    # Pfad: 100% Match

class TestFindRecipesPaginierung:
    def testErsteSeite()            # Pfad: index=0
    def testZweiteSeite()           # Pfad: index=1
    def testLeereSeite()            # Pfad: index jenseits der Daten
    def testGenauZwoelfRezepte()    # Grenzfall: exakt 12 Einträge
```

Jede Verzweigung in `findRecipes()` wird mindestens einmal ausgeführt → hohe Branch Coverage.

---

### Schlechtes Beispiel: `AuthService.py` – ungetestete Pfade

```python
def validateRefreshToken(token: str) -> dict | None:
    entry = AccountDAO.getRefreshToken(token)
    if entry is None:           # ← Branch A
        return None
    expiresAt = datetime.fromisoformat(entry["expiresAt"])
    if expiresAt.tzinfo is None:  # ← Branch B (timezone-Edge-Case)
        expiresAt = expiresAt.replace(tzinfo=timezone.utc)
    if expiresAt < datetime.now(timezone.utc):  # ← Branch C
        return None
    return entry
```

Wenn es **keinen Test** gibt, der Branch B (fehlende Zeitzone) oder Branch C (abgelaufener Token) explizit auslöst, ist die Branch Coverage gering – obwohl alle Zeilen vielleicht einmal ausgeführt wurden.

**Verbesserung durch Tests:**

```python
def test_validateRefreshToken_abgelaufen():
    """Branch C: Token ist in der Vergangenheit → soll None zurückgeben."""
    vergangenheit = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    with patch.object(AccountDAO, "getRefreshToken", return_value={
        "expiresAt": vergangenheit, "email": "test@test.de", "AccountID": 1
    }):
        result = validateRefreshToken("fake-token")
        assert result is None

def test_validateRefreshToken_ohne_timezone():
    """Branch B: Zeitstempel ohne tzinfo → soll trotzdem korrekt verglichen werden."""
    zukunft = (datetime.now() + timedelta(days=1)).isoformat()  # kein UTC
    with patch.object(AccountDAO, "getRefreshToken", return_value={
        "expiresAt": zukunft, "email": "test@test.de", "AccountID": 1
    }):
        result = validateRefreshToken("fake-token")
        assert result is not None
```

---

### Wo ist eine niedrige Coverage akzeptabel?

`AuthRoutes.py` hat viel Boilerplate-Code für HTTP-Fehler:

```python
@router.post("/auth/forgot-password")
async def forgotPassword(body: ForgotPasswordRequest):
    konto = AccountDAO.getAccountByEmail(body.email)
    if konto is not None:
        token = AuthService.createPasswordResetToken(konto["id"])
        resetLink = f"{FRONTEND_URL}/reset-password?token={token}"
        try:
            sendPasswordResetEmail(body.email, konto["name"], resetLink)
        except Exception as e:
            logger.warning("Reset-Mail konnte nicht gesendet werden: %s", e)
    return {"detail": "Falls die E-Mail existiert, wurde ein Link versendet."}
```

Der `except`-Block ist bewusst ein "best effort" – wenn die E-Mail nicht gesendet werden kann, soll die Anfrage trotzdem erfolgreich sein. Diesen Pfad zu testen würde nur externe Abhängigkeiten mocken, ohne wirklichen Mehrwert. **Kein Handlungsbedarf.**

---

## 3. Zyklomatische Komplexität (Cyclomatic Complexity)

### Was ist die Metrik?

Zyklomatische Komplexität zählt die Anzahl unabhängiger Pfade durch eine Funktion. Jedes `if`, `elif`, `for`, `while`, `and`, `or` erhöht den Wert um 1. Startwert ist 1.

| Wert | Bewertung |
|------|-----------|
| 1–5  | Einfach, gut testbar |
| 6–10 | Mittel, noch akzeptabel |
| 11+  | Komplex, Refactoring empfohlen |

**Ziel:** Funktionen sollen wenige, klar trennbare Pfade haben.

---

### Beispiel mit hoher Komplexität: `validatePassword()` in `Auth.py`

```python
def validatePassword(pw: str) -> str | None:
    if len(pw) < 8:                          # +1 → Komplexität: 2
        return "Passwort muss mindestens 8 Zeichen lang sein."
    if not re.search(r"[A-Z]", pw):          # +1 → 3
        return "Passwort muss mindestens einen Großbuchstaben enthalten."
    if not re.search(r"[a-z]", pw):          # +1 → 4
        return "Passwort muss mindestens einen Kleinbuchstaben enthalten."
    if not re.search(r"[0-9]", pw):          # +1 → 5
        return "Passwort muss mindestens eine Zahl enthalten."
    if not re.search(r"[^A-Za-z0-9]", pw):  # +1 → 6
        return "Passwort muss mindestens ein Sonderzeichen enthalten."
    return None
```

**Komplexität: 6** – an der Grenze. Jede Regel ist aber eine eigenständige fachliche Anforderung. Eine Zusammenfassung (z. B. Loop über Regeln) würde Lesbarkeit opfern ohne echten Gewinn. **Kein Handlungsbedarf.**

---

### Beispiel mit reduzierter Komplexität durch SRP-Refactoring

`updateUser()` in `UserService.py` **vor** dem Refactoring (hypothetisch, alles in einer Funktion):

```python
# Vor SRP-Refactoring: eine Funktion macht alles
def updateUser(konto_id, current_email, data):
    if data.email:                              # +1
        if not re.match(r"^[^\s@]+@...$", data.email):  # +1
            raise ValueError("Ungültige E-Mail")
        AccountDAO.updateAccount(konto_id, email=data.email)

    if data.currentPassword and data.newPassword:    # +1  (and = +1 → gesamt +2)
        account = AccountDAO.getAccountById(konto_id)
        if not bcrypt.checkpw(...):             # +1
            raise ValueError("Passwort falsch")
        if len(data.newPassword) < 8:           # +1
            raise ValueError("Zu kurz")
        if not re.search(r"[A-Z]", data.newPassword): # +1
            raise ValueError("Kein Großbuchstabe")
        # ... weitere Passwort-Checks
        AccountDAO.updateAccount(konto_id, password_hash=...)
        try:
            sendPasswordChangedEmail(...)       # try/except = +1
        except Exception:
            pass
# Komplexität: ~9
```

**Nach dem SRP-Refactoring** (aktueller Stand):

```python
# UserService.py – delegiert Validierung an spezialisierte Funktionen
def updateUser(konto_id: int, current_email: str, data) -> None:
    if data.email:                              # +1
        error = validateEmail(data.email)       # Komplexität steckt in Auth.py
        if error:                               # +1
            raise ValueError(error)
        AccountDAO.updateAccount(konto_id, email=data.email)

    if data.currentPassword and data.newPassword:  # +1 (+1 für 'and') → +2
        account = AccountDAO.getAccountById(konto_id)
        if not verifyPassword(data.currentPassword, account["hashedPassword"]):  # +1
            raise ValueError("Aktuelles Passwort ist falsch")
        error = validatePassword(data.newPassword) # Komplexität steckt in Auth.py
        if error:                               # +1
            raise ValueError(error)
        AccountDAO.updateAccount(konto_id, password_hash=hashPassword(data.newPassword))
        try:
            sendPasswordChangedEmail(...)
        except Exception as e:                  # +1
            logger.warning(...)
# Komplexität: ~7  (statt ~9)
```

Die Komplexität **sinkt**, weil `validateEmail()` und `validatePassword()` die Detaillogik kapseln. `updateUser()` orchestriert nur noch – es kennt nicht mehr jeden einzelnen Passwortregeln.

---

### Zusammenfassung: Wann ist hohe Komplexität akzeptabel?

| Funktion | Komplexität | Handlungsbedarf? | Begründung |
|---|---|---|---|
| `validatePassword()` | 6 | Nein | Jede Bedingung = eine fachliche Regel, keine Vereinfachung möglich |
| `updateUser()` | 7 | Nein | Nach SRP-Refactoring bereits verbessert, Delegation an Services |
| `validateRefreshToken()` | 4 | Nein | Klar, linear, gut lesbar |
| `resetPassword()` (Route) | 5 | Nein | HTTP-Handler-Boilerplate, gehört zur Route-Schicht |

---

## Zusammenfassung aller drei Metriken

| Metrik | Werkzeug | Zielwert | Gutes Beispiel im Projekt | Verbesserungspotenzial |
|---|---|---|---|---|
| **Duplikate** | SonarQube, Lizard | < 3 % duplizierter Code | `_toRecipe()` nach Refactoring | `_initRecipes` / `getMatchingRecipeNames` vor Refactoring |
| **Coverage** | pytest-cov | ≥ 80 % (Lines), ≥ 70 % (Branches) | `test_recipe_sucuk.py` (vollständig) | `AuthService.py` – Token-Ablauf nicht getestet |
| **Zyklom. Komplexität** | Radon, Lizard | ≤ 10 pro Funktion | `_scoreRecipes()`: Komplexität 3 | `validatePassword()`: 6, aber akzeptabel |
