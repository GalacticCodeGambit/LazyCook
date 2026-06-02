import sqlite3
import logging
from contextlib import contextmanager
from pathlib import Path
import os

logger = logging.getLogger(__name__)

# Verwende die Datenbank aus dem data-Ordner
DB_PATH = Path(__file__).parent.parent / "data" / "LazyCookDB.sqlite3"

# Stelle sicher, dass das Verzeichnis existiert
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def getConnection() -> sqlite3.Connection:
    """Erstellt eine neue SQLite-Connection mit Row-Factory."""
    con = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode = WAL")
    con.execute("PRAGMA foreign_keys = ON")
    return con


@contextmanager
def getDB():
    """Context-Manager: öffnet Connection, committed bei Erfolg, rollt bei Fehler zurück."""
    con = getConnection()
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def initDB():
    """Erstellt alle Tabellen, falls sie noch nicht existieren."""
    with getDB() as con:
        cur = con.cursor()

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Account (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email VARCHAR(250) NOT NULL UNIQUE,
                        name TEXT NOT NULL,
                        hashedPassword TEXT NOT NULL,
                        createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)

        # Refresh Tokens – pro Account können mehrere existieren (z.B. verschiedene Geräte)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS RefreshToken (
                                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                AccountID INTEGER NOT NULL,
                                                                token TEXT NOT NULL UNIQUE,
                                                                expiresAt TIMESTAMP NOT NULL,
                                                                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                                FOREIGN KEY (AccountID) REFERENCES Account (id) ON DELETE CASCADE
                        )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Ingredient (
                                                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                         name TEXT UNIQUE NOT NULL,
                                                         amountType VARCHAR(30) NOT NULL
                        )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Author (
                                                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                             name TEXT UNIQUE NOT NULL
                    )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Recipe (
                                                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          name TEXT UNIQUE NOT NULL,
                                                          description nvarchar(20000),
                                                          vid INTEGER,
                                                          FOREIGN KEY (vid) REFERENCES Author (id) ON DELETE CASCADE
                        )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Exists_from (
                        zid INTEGER NOT NULL,
                        rid INTEGER NOT NULL,
                        amount DECIMAL(10,2) NOT NULL,
                        FOREIGN KEY (zid) REFERENCES Ingredient (id) ON DELETE CASCADE,
                        FOREIGN KEY (rid) REFERENCES Recipe (id) ON DELETE CASCADE,
                        UNIQUE (zid, rid)
                        )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Favorites (
                        AccountID INTEGER NOT NULL,
                        rid INTEGER NOT NULL,
                        FOREIGN KEY (AccountID) REFERENCES Account (id) ON DELETE CASCADE,
                        FOREIGN KEY (rid) REFERENCES Recipe (id) ON DELETE CASCADE,
                        UNIQUE (AccountID, rid)
                        )
                    """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS IngredientUsage (
                                                                   AccountID INTEGER NOT NULL,
                                                                   name TEXT NOT NULL,
                                                                   displayName TEXT NOT NULL,
                                                                   count INTEGER NOT NULL DEFAULT 1,
                                                                   lastUnit TEXT,
                                                                   lastUsedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                                   PRIMARY KEY (AccountID, name),
                                                                   FOREIGN KEY (AccountID) REFERENCES Account (id) ON DELETE CASCADE
                        )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS PasswordResetToken (
                                                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                              kontoID INTEGER NOT NULL,
                                                              tokenHash TEXT NOT NULL UNIQUE,
                                                              expiresAt TIMESTAMP NOT NULL,
                                                              usedAt TIMESTAMP,
                                                              createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                              FOREIGN KEY (kontoID) REFERENCES Account (id) ON DELETE CASCADE
                        )
                    """)

    logger.info("Datenbank-Tabellen erfolgreich initialisiert")


# ── Account-Operationen ──────────────────────────────────────────


def createAccount(email: str, name: str, hashedPassword: str) -> dict | None:
    """Legt ein neues Account an. Gibt die Account-Daten zurück oder None bei Duplikat."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("SELECT 1 FROM Account WHERE email = ? LIMIT 1", (email,))
        if cur.fetchone():
            return None
        cur.execute(
            "INSERT INTO Account (email, name, hashedPassword) VALUES (?, ?, ?)",
            (email, name, hashedPassword),
        )
        return {"id": cur.lastrowid, "email": email, "name": name}


def getAccountByEmail(email: str) -> dict | None:
    """Gibt Account-Daten inkl. hashedPassword zurück, oder None."""
    con = getConnection()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT id, email, name, hashedPassword FROM Account WHERE email = ?",
            (email,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        con.close()


# ── Refresh-Token-Operationen ──────────────────────────────────


def saveRefreshToken(AccountID: int, token: str, expiresAt: str) -> None:
    """Speichert einen neuen Refresh Token in der Datenbank."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO RefreshToken (AccountID, token, expiresAt) VALUES (?, ?, ?)",
            (AccountID, token, expiresAt),
        )


def getRefreshToken(token: str) -> dict | None:
    """Gibt den Refresh-Token-Eintrag zurück, oder None."""
    con = getConnection()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT rt.id, rt.AccountID, rt.token, rt.expiresAt, k.email, k.name "
            "FROM RefreshToken rt JOIN Account k ON rt.AccountID = k.id "
            "WHERE rt.token = ?",
            (token,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        con.close()


def deleteRefreshToken(token: str) -> None:
    """Löscht einen einzelnen Refresh Token (Logout)."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM RefreshToken WHERE token = ?", (token,))


def deleteAllRefreshTokens(AccountID: int) -> None:
    """Löscht alle Refresh Tokens eines Accounts (Logout von allen Geräten)."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM RefreshToken WHERE AccountID = ?", (AccountID,))


def deleteAccount(email: str) -> bool:
    """Löscht ein Account anhand der E-Mail. Refresh Tokens werden via CASCADE mitgelöscht."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM Account WHERE email = ?", (email,))
        return cur.rowcount > 0


def updateAccount(konto_id: int, email: str = None, password_hash: str = None) -> None:
    """Aktualisiert E-Mail und/oder Passwort eines Accounts."""
    with getDB() as con:
        cur = con.cursor()
        if email:
            cur.execute("UPDATE Account SET email = ? WHERE id = ?", (email, konto_id))
        if password_hash:
            cur.execute(
                "UPDATE Account SET hashedPassword = ? WHERE id = ?",
                (password_hash, konto_id),
            )


def cleanupExpiredTokens() -> None:
    """Löscht alle abgelaufenen Refresh Tokens."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM RefreshToken WHERE expiresAt < datetime('now')")


def addRecipe(name: str, description: str, vid: int) -> int:
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO Recipe (name, description) VALUES (?, ?)",
            (name, description),
        )
        return cur.lastrowid


def addIngredientToRecipe(zid: int, rid: int, amount: float) -> None:
    if not zid or not rid:
        return False
    try:
        with getDB() as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Exists_from (zid, rid, amount) VALUES (?, ?, ?)",
                (zid, rid, amount),
            )
    except Exception as e:
        return False


def addIngredient(name: str, amountType: str) -> int:
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO Ingredient (name, amountType) VALUES (?, ?)",
            (name, amountType),
        )
        return cur.lastrowid


def getIngredientByName(name: str):
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            """
                    SELECT id, amountType
                    FROM Ingredient
                    WHERE name = ?
                    """,
            (name,),
        )
        row = cur.fetchone()
        return dict(row) if row else None


def getRecipe(recipeID: int) -> dict | None:
    """Gibt eine Liste aller Rezepte zurück."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            """
                    SELECT name, description
                    FROM Recipe
                    WHERE id = ?
                    """,
            (recipeID,),
        )
        row = cur.fetchone()
        return dict(row) if row else None


def getAllRecipes() -> list[dict]:
    with getDB() as con:
        cur = con.cursor()
        cur.execute("""
                    SELECT id, name, description
                    FROM Recipe
                    """)
        rows = cur.fetchall()
        return [dict(row) for row in rows]



def getAllIngredientsForRecipe(rid: int):
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT 
                Ingredient.name, 
                Exists_from.amount,
                Ingredient.amountType
            FROM Ingredient
            JOIN Exists_from ON Ingredient.id = Exists_from.zid
            JOIN Recipe ON Exists_from.rid = Recipe.id
            WHERE Exists_from.rid = ?
        """,
            (rid,),
        )  # Note the comma here!
        rows = cur.fetchall()
        return [dict(row) for row in rows]


def getAllocatedRecipes(name: str) -> list[dict]:

    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            """
                    SELECT rid
                    FROM Exists_from
                    INNER JOIN Ingredient ON Exists_from.zid = Ingredient.id
                    WHERE Ingredient.name = ?
                    """,
            (name,),
        )
        rows = cur.fetchall()
        return [dict(row) for row in rows]

def getAllIngredients() -> list[dict]:
    with getDB() as con:
        cur = con.cursor()
        cur.execute("""
                    SELECT id, name, amountType
                    FROM Ingredient
                    """)
        rows = cur.fetchall()
        return [dict(row) for row in rows]

"""
# --- 1. Fresh Pesto Pasta ---
r1 = addRecipe("Fresh Pesto Pasta", "Classic Italian basil pesto with linguine.", 301)
i1 = addIngredient("Linguine", "grams")
i2 = addIngredient("Fresh Basil", "grams")
i3 = addIngredient("Pine Nuts", "grams")
i4 = addIngredient("Parmesan", "grams")
addIngredientToRecipe(i1, r1, 200.0)
addIngredientToRecipe(i2, r1, 50.0)
addIngredientToRecipe(i3, r1, 30.0)
addIngredientToRecipe(i4, r1, 40.0)

# --- 2. Beef Tacos ---
r2 = addRecipe("Beef Tacos", "Street-style seasoned beef tacos.", 302)
i5 = addIngredient("Corn Tortillas", "pieces")
i6 = addIngredient("Ground Beef", "grams")
i7 = addIngredient("Cumin", "teaspoons")
addIngredientToRecipe(i5, r2, 3.0)
addIngredientToRecipe(i6, r2, 150.0)
addIngredientToRecipe(i7, r2, 1.0)

# --- 3. Greek Salad ---
r3 = addRecipe("Greek Salad", "Refreshing cucumber and feta salad.", 303)
i8 = addIngredient("Cucumber", "pieces")
i9 = addIngredient("Feta Cheese", "grams")
i10 = addIngredient("Kalamata Olives", "pieces")
addIngredientToRecipe(i8, r3, 1.0)
addIngredientToRecipe(i9, r3, 100.0)
addIngredientToRecipe(i10, r3, 10.0)

# --- 4. Mushroom Risotto ---
r4 = addRecipe("Mushroom Risotto", "Creamy arborio rice with wild mushrooms.", 304)
i11 = addIngredient("Arborio Rice", "grams")
i12 = addIngredient("Mushrooms", "grams")
i13 = addIngredient("Vegetable Broth", "ml")
addIngredientToRecipe(i11, r4, 150.0)
addIngredientToRecipe(i12, r4, 200.0)
addIngredientToRecipe(i13, r4, 500.0)

# --- 5. French Toast ---
r5 = addRecipe("French Toast", "Brioche soaked in cinnamon egg wash.", 305)
i14 = addIngredient("Brioche Bread", "slices")
i15 = addIngredient("Cinnamon", "teaspoons")
# Reusing 'Egg' and 'Milk' from previous datasets if they exist
addIngredientToRecipe(14, r5, 2.0) # Brioche
addIngredientToRecipe(2, r5, 2.0)  # Egg (zid 2)
addIngredientToRecipe(15, r5, 0.5) # Cinnamon

# --- 6. Margherita Pizza ---
r6 = addRecipe("Margherita Pizza", "Simple pizza with tomato, mozzarella, and basil.", 306)
i16 = addIngredient("Pizza Dough", "grams")
i17 = addIngredient("Mozzarella", "grams")
addIngredientToRecipe(i16, r6, 250.0)
addIngredientToRecipe(i17, r6, 120.0)
addIngredientToRecipe(i2, r6, 10.0) # Basil

# --- 7. Salmon with Asparagus ---
r7 = addRecipe("Baked Salmon", "Lemon-butter salmon with roasted asparagus.", 307)
i18 = addIngredient("Salmon Fillet", "grams")
i19 = addIngredient("Asparagus", "grams")
i20 = addIngredient("Lemon", "pieces")
addIngredientToRecipe(i18, r7, 200.0)
addIngredientToRecipe(i19, r7, 150.0)
addIngredientToRecipe(i20, r7, 0.5)

# --- 8. Chicken Stir-fry ---
r8 = addRecipe("Chicken Stir-fry", "Quick soy-ginger chicken and veggies.", 308)
i21 = addIngredient("Soy Sauce", "ml")
i22 = addIngredient("Ginger", "grams")
i23 = addIngredient("Broccoli", "grams")
addIngredientToRecipe(5, r8, 200.0)  # Chicken Breast (zid 5)
addIngredientToRecipe(i21, r8, 30.0)
addIngredientToRecipe(i22, r8, 10.0)
addIngredientToRecipe(i23, r8, 100.0)

# --- 9. Guacamole ---
r9 = addRecipe("Guacamole", "Chunky avocado dip with lime.", 309)
i24 = addIngredient("Avocado", "pieces")
i25 = addIngredient("Lime Juice", "ml")
addIngredientToRecipe(i24, r9, 3.0)
addIngredientToRecipe(i25, r9, 15.0)
addIngredientToRecipe(4, r9, 0.25) # Salt

# --- 10. Chocolate Chip Cookies ---
r10 = addRecipe("Chocolate Cookies", "Chewy cookies with dark chocolate chips.", 310)
i26 = addIngredient("Chocolate Chips", "grams")
i27 = addIngredient("Vanilla Extract", "ml")
addIngredientToRecipe(1, r10, 250.0)  # Flour
addIngredientToRecipe(14, r10, 150.0) # Butter
addIngredientToRecipe(11, r10, 100.0) # Sugar
addIngredientToRecipe(i26, r10, 100.0)
addIngredientToRecipe(i27, r10, 5.0)
"""


# ── Password-Reset-Token-Operationen ───────────────────────────


def savePasswordResetToken(kontoID: int, tokenHash: str, expiresAt: str) -> None:
    """Invalidiert alte Tokens des Kontos und speichert einen neuen."""
    with getDB() as con:
        cur = con.cursor()
        # Alte, ungenutzte Tokens für dieses Konto invalidieren
        cur.execute(
            "UPDATE PasswordResetToken SET usedAt = CURRENT_TIMESTAMP "
            "WHERE kontoID = ? AND usedAt IS NULL",
            (kontoID,),
        )
        cur.execute(
            "INSERT INTO PasswordResetToken (kontoID, tokenHash, expiresAt) VALUES (?, ?, ?)",
            (kontoID, tokenHash, expiresAt),
        )


def getPasswordResetToken(tokenHash: str) -> dict | None:
    con = getConnection()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT id, kontoID, tokenHash, expiresAt, usedAt "
            "FROM PasswordResetToken WHERE tokenHash = ?",
            (tokenHash,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        con.close()


def markResetTokenUsed(tokenID: int) -> None:
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE PasswordResetToken SET usedAt = CURRENT_TIMESTAMP WHERE id = ?",
            (tokenID,),
        )


def updateKontoPassword(konto_id: int, hashed_password: str) -> None:
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE Account SET hashedPassword = ? WHERE id = ?",
            (hashed_password, konto_id),
        )


# ── Ingredient-Usage-Operationen ───────────────────────────────


def incrementIngredientUsage(AccountID: int, name: str, unit: str | None) -> None:
    """Erhöht den Usage-Counter für eine Zutat um 1, aktualisiert lastUnit und lastUsedAt.
    Legt einen neuen Eintrag an, falls die Zutat für diesen Account noch nicht existiert.
    Der Name wird normalisiert (trim + lowercase) für den Primary Key, displayName behält
    die Originalschreibweise der letzten Eingabe.
    """
    displayName = (name or "").strip()
    if not displayName:
        return
    normalizedName = displayName.lower()
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO IngredientUsage (AccountID, name, displayName, count, lastUnit, lastUsedAt)
            VALUES (?, ?, ?, 1, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(AccountID, name) DO UPDATE SET
                count = count + 1,
                displayName = excluded.displayName,
                lastUnit = excluded.lastUnit,
                lastUsedAt = CURRENT_TIMESTAMP
            """,
            (AccountID, normalizedName, displayName, unit),
        )


def getTopIngredients(AccountID: int, limit: int = 5) -> list[dict]:
    """Liefert die meistgenutzten Zutaten des Users.
    Sortierung Hybrid: erst nach count DESC, dann nach lastUsedAt DESC als Tie-Breaker.
    """
    con = getConnection()
    try:
        cur = con.cursor()
        cur.execute(
            """
            SELECT displayName, lastUnit, count, lastUsedAt
            FROM IngredientUsage
            WHERE AccountID = ?
            ORDER BY count DESC, lastUsedAt DESC
            LIMIT ?
            """,
            (AccountID, limit),
        )
        return [dict(row) for row in cur.fetchall()]
    finally:
        con.close()


def getAccountById(konto_id: int) -> dict | None:
    """Gibt Account-Daten anhand der ID zurück, oder None."""
    con = getConnection()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT id, email, name, hashedPassword FROM Account WHERE id = ?",
            (konto_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        con.close()

