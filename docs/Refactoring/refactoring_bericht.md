# Refactoring-Bericht: Schichtenarchitektur & SRP

**Datum:** 03.06.2026  
**Scope:** Backend (`/backend`)  
**Alle 74 Tests bestanden ✅**

---

## 1. Motivation

Das Backend verstieß an mehreren Stellen gegen die Schichtenarchitektur und das Single Responsibility Principle:

- **Domain-Objekte griffen direkt auf die Datenbank zu** (`Recipe.saveInDB()`, `Ingredient.saveInDB()`, `Ingredient.formatIngredients()`)
- **Kein Service-Layer**: `Routes.py` orchestrierte Datenbankzugriffe, Validierungen und E-Mail-Versand in einer Funktion
- **`Auth.py` mischte** JWT-Kryptographie, Token-Verwaltung und Datenbankzugriffe
- **`Database.py`** enthielt alle SQL-Funktionen (Account, Rezept, Zutat, Token) in einer einzigen Datei

---

## 2. Neue Struktur

```
backend/
├── domain/                  ← Reine Datenobjekte, kein DB-Zugriff
│   ├── ingredient.py
│   ├── recipe.py
│   └── person.py
├── dao/                     ← Data Access Objects (SQL-Logik)
│   ├── account_dao.py       ← Account, RefreshToken, PasswordResetToken
│   ├── recipe_dao.py        ← Recipe, Exists_from
│   └── ingredient_dao.py    ← Ingredient, IngredientUsage
├── services/                ← Geschäftslogik
│   ├── auth_service.py      ← Token-Orchestrierung
│   ├── user_service.py      ← Account-Verwaltung
│   └── recipe_service.py    ← Rezeptsuche (SUCUK + SearchRecipeNames)
├── routes/                  ← HTTP-Endpunkte (nur Ein-/Ausgabe)
│   ├── auth.py
│   ├── users.py
│   └── recipes.py
├── Auth.py                  ← Krypto, Validierung, FastAPI-Dependency
├── Database.py              ← Verbindungsmanagement + initDB (unverändert)
├── Models.py                ← Pydantic-Schemas
└── EmailService.py          ← E-Mail-Versand
```

---

## 3. Geänderte Dateien im Überblick

| Datei | Aktion | Begründung |
|---|---|---|
| `Recipe.py` | Deprecation-Stub | `saveInDB()` und DB-Importe entfernt → `domain/recipe.py` |
| `Ingredient.py` | Deprecation-Stub | `saveInDB()`, `formatIngredients()`, DB-Importe → `domain/` + `dao/` |
| `Person.py` | Deprecation-Stub | Verschoben nach `domain/person.py` |
| `RecipeSUCUK.py` | Deprecation-Stub | Verschoben nach `services/recipe_service.py` |
| `SearchRecipeNames.py` | Deprecation-Stub | In `services/recipe_service.py` integriert |
| `Routes.py` | Deprecation-Stub | Aufgeteilt in `routes/auth.py`, `routes/users.py`, `routes/recipes.py` |
| `Auth.py` | Reduziert | Token-Orchestrierung → `services/auth_service.py`; DB-Importe → `dao/account_dao.py` |
| `Database.py` | Bereinigt | Nur `getConnection()`, `getDB()`, `initDB()` behalten; SQL-Funktionen → DAOs |
| `LazyCookAdministration.py` | Aktualisiert | Importiert aus `routes/` statt `Routes.py` |
| `ImportRecipes.py` | Aktualisiert | Importiert aus `domain/` und `dao/` |
| `tests/test_database.py` | Aktualisiert | Importiert aus `dao.*` statt `Database` |
| `tests/test_recipe_sucuk.py` | Aktualisiert | Importiert aus `services.recipe_service` + `domain.ingredient` |
| `tests/test_auth_tokens.py` | Aktualisiert | Importiert aus `services.auth_service` statt `Auth` |

---

## 4. Konkrete Vorher/Nachher-Beispiele

### Beispiel 1: Domain-Objekt ohne DB-Zugriff

**Vorher (`Recipe.py`):**
```python
from Database import addIngredientToRecipe, addRecipe, getIngredientByName

class Recipe:
    def saveInDB(self) -> bool:           # ❌ Domain ruft DB auf
        rid = addRecipe(self.__name, ...)
        for ingredient in self.__ingredients:
            result = getIngredientByName(ingredient.getName())
            zid = result["id"]
            addIngredientToRecipe(zid, rid, ingredient.getAmount())
        return True
```

**Nachher (`domain/recipe.py`):**
```python
class Recipe:
    # Nur Attribute und Getter/Setter – kein DB-Import, kein saveInDB()
    def getName(self) -> str: return self.__name
    def getRating(self) -> float: return self.__rating
    def incrementMatching(self): self.__matching += 1
    # ...
```

**Das Speichern übernimmt nun `ImportRecipes.py` via `dao/recipe_dao.py`:**
```python
rid = recipe_dao.addRecipe(recipe.getName(), recipe.getDescription(), None)
for ingredient in recipe.getIngredients():
    result = ingredient_dao.getIngredientByName(ingredient.getName())
    recipe_dao.addIngredientToRecipe(result["id"], rid, ingredient.getAmount())
```

---

### Beispiel 2: Route delegiert an Service

**Vorher (`Routes.py` – `updateCurrentUser`):**
```python
@router.patch("/users/me")
async def updateCurrentUser(data, currentUser):
    account = getAccountByEmail(currentUser.email)    # ❌ DB-Zugriff in Route
    if data.currentPassword:
        if not verifyPassword(...): raise HTTPException(...)  # ❌ Logik in Route
        newHash = hashPassword(data.newPassword)
        updateAccount(account["id"], password_hash=newHash)   # ❌ DB-Zugriff in Route
        sendPasswordChangedEmail(...)                          # ❌ E-Mail in Route
    return {"success": True}
```

**Nachher (`routes/users.py`):**
```python
@router.patch("/users/me")
async def updateCurrentUser(data, currentUser):
    account = account_dao.getAccountByEmail(currentUser.email)
    try:
        user_service.updateUser(account["id"], account["email"], data)  # ✅ Delegation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"success": True}
```

**Logik liegt in `services/user_service.py`:**
```python
def updateUser(konto_id, current_email, data):
    if data.currentPassword and data.newPassword:
        account = account_dao.getAccountById(konto_id)
        if not verifyPassword(data.currentPassword, account["hashedPassword"]):
            raise ValueError("Aktuelles Passwort ist falsch")
        account_dao.updateAccount(konto_id, password_hash=hashPassword(data.newPassword))
        sendPasswordChangedEmail(...)
```

---

### Beispiel 3: Auth.py – Aufgabenreduktion

**Vorher (`Auth.py`):** JWT + Hashing + Validierung + Refresh-Token-DB + Password-Reset-DB + FastAPI-Dependency

**Nachher (`Auth.py`):** nur JWT + Hashing + Validierung + FastAPI-Dependency  
**Verschoben nach `services/auth_service.py`:** `createTokenPair`, `createRefreshToken`, `validateRefreshToken`, `createPasswordResetToken`, `validatePasswordResetToken`, `hashResetToken`

---

### Beispiel 4: `RecipeSUCUK` + `SearchRecipeNames` → ein Service

**Vorher:** Zwei separate Dateien mit doppeltem `getAllRecipes()`-Import und eigener Initialisierungslogik.

**Nachher (`services/recipe_service.py`):**
```python
def findRecipes(ingredients, index): ...
def getMatchingRecipeNames(searchTerm): ...
def _initRecipes(): ...   # gemeinsam genutzt
def _scoreRecipes(): ...
```

---

## 5. Test-Ergebnis

```
74 passed in 3.98s
```

Keine Funktionalität wurde durch das Refactoring beeinträchtigt.
