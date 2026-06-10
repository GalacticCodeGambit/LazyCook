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
def getAllRecipesPaginated(offset: int) -> list[dict]:
    with getDB() as con:
        cur = con.cursor()
        cur.execute("""
                    SELECT r.id, r.name, r.description
                    FROM Recipe r
                    ORDER BY r.name
                        LIMIT 12 OFFSET ?
                    """, (offset,))
        return [dict(row) for row in cur.fetchall()]


def searchRecipesByIngredients(likeConditions: str, likeParams: list, offset: int) -> list[dict]:
    with getDB() as con:
        cur = con.cursor()
        cur.execute(f"""
            SELECT
                r.id, r.name, r.description,
                COUNT(DISTINCT CASE WHEN {likeConditions} THEN i.id END) AS matching,
                COUNT(DISTINCT ef.zid) AS total
            FROM Recipe r
            LEFT JOIN Exists_from ef ON ef.rid = r.id
            LEFT JOIN Ingredient i ON i.id = ef.zid
            GROUP BY r.id
            ORDER BY matching DESC, r.name
            LIMIT 12 OFFSET ?
        """, (*likeParams, offset))
        return [dict(row) for row in cur.fetchall()]

def getAllRecipesWithIngredients() -> list[dict]:
    with getDB() as con:
        cur = con.cursor()
        cur.execute("""
                    SELECT r.id, r.name, r.description,
                           i.name as ing_name, ef.amount, i.amountType
                    FROM Recipe r
                             LEFT JOIN Exists_from ef ON ef.rid = r.id
                             LEFT JOIN Ingredient i ON i.id = ef.zid
                    ORDER BY r.id
                    """)
        rows = cur.fetchall()

    recipes = {}
    for row in rows:
        rid = row["id"]
        if rid not in recipes:
            recipes[rid] = {"id": rid, "name": row["name"], "description": row["description"], "ingredients": []}
        if row["ing_name"]:
            recipes[rid]["ingredients"].append({
                "name": row["ing_name"],
                "amount": row["amount"],
                "amountType": row["amountType"]
            })
    return list(recipes.values())