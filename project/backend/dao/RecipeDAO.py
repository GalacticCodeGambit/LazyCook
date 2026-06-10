"""
recipe_dao.py – Data Access Object für Recipe und Exists_from
"""

from core.Database import getDB


def addRecipe(name: str, description: str) -> int:
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO Recipe (name, description) VALUES (?, ?)",
            (name, description),
        )
        return cur.lastrowid


def getRecipe(recipeID: int) -> dict | None:
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT name, description FROM Recipe WHERE id = ?",
            (recipeID,),
        )
        row = cur.fetchone()
        return dict(row) if row else None


def getAllRecipes() -> list[dict]:
    with getDB() as con:
        cur = con.cursor()
        cur.execute("SELECT id, name, description FROM Recipe")
        rows = cur.fetchall()
        return [dict(row) for row in rows]


def getAllIngredientsForRecipe(rid: int) -> list[dict]:
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT Ingredient.name, Exists_from.amount, Ingredient.amountType
            FROM Ingredient
            JOIN Exists_from ON Ingredient.id = Exists_from.zid
            WHERE Exists_from.rid = ?
            """,
            (rid,),
        )
        return [dict(row) for row in cur.fetchall()]


def addIngredientToRecipe(rid: int, zid: int, amount: float) -> bool:
    if not zid or not rid:
        return False
    try:
        with getDB() as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Exists_from (zid, rid, amount) VALUES (?, ?, ?)",
                (zid, rid, amount),
            )
        return True
    except Exception:
        return False


def getAllocatedRecipes(name: str) -> list[dict]:
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT rid FROM Exists_from
            INNER JOIN Ingredient ON Exists_from.zid = Ingredient.id
            WHERE Ingredient.name = ?
            """,
            (name,),
        )
        return [dict(row) for row in cur.fetchall()]
