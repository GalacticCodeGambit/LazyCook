"""
ingredient_dao.py – Data Access Object für Ingredient und IngredientUsage
"""

from core.Database import getDB, getConnection
from domain.ingredient import Ingredient


def addIngredient(name: str, amountType: str) -> int:
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO Ingredient (name, amountType) VALUES (?, ?)",
            (name, amountType),
        )
        return cur.lastrowid


def getIngredientByName(name: str) -> dict | None:
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT id, amountType FROM Ingredient WHERE name = ?",
            (name,),
        )
        row = cur.fetchone()
        return dict(row) if row else None


def getAllIngredients() -> list[dict]:
    with getDB() as con:
        cur = con.cursor()
        cur.execute("SELECT id, name, amountType FROM Ingredient")        return [dict(row) for row in cur.fetchall()]


def getIngredientsForRecipe(rid: int) -> list[Ingredient]:
    """Gibt die Zutaten eines Rezepts als Ingredient-Objekte zurück."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT Ingredient.name, Exists_from.amount
            FROM Ingredient
            JOIN Exists_from ON Ingredient.id = Exists_from.zid
            WHERE Exists_from.rid = ?
            """,
            (rid,),
        )
        return [Ingredient(row["name"], row["amount"]) for row in cur.fetchall()]


def incrementIngredientUsage(AccountID: int, name: str, unit: str | None) -> None:
    """Erhöht den Usage-Counter für eine Zutat um 1."""
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
    """Liefert die meistgenutzten Zutaten des Users."""
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
