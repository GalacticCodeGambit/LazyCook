import json
import re
import sys
import os

sys.path.insert(0, '/app')
os.chdir('/app')

from dao.RecipeDAO import addRecipe, addIngredientToRecipe
from dao.IngredientDAO import addIngredient, getIngredientByName
from core.Database import getConnection, initDB

def getOrCreateIngredient(name: str) -> int:
    existing = getIngredientByName(name)
    if existing:
        return existing["id"]
    return addIngredient(name, "mixed")

def extractIngredientName(raw: str) -> str:
    """Extrahiert den Zutatennamen aus einem String wie '41 g Butter' → 'Butter'"""
    # Entferne führende Mengenangaben: Zahlen, Einheiten, Sonderzeichen
    cleaned = re.sub(r'^[\d\s.,/]+', '', raw).strip()
    # Entferne bekannte Einheiten am Anfang
    units = ['g ', 'kg ', 'ml ', 'l ', 'EL ', 'TL ', 'Stück ', 'Prise ',
             'tsp ', 'tbsp ', 'cup ', 'oz ', 'lb ', 'cl ']
    for unit in units:
        if cleaned.startswith(unit):
            cleaned = cleaned[len(unit):].strip()
    # Alles nach Klammer oder Komma abschneiden
    cleaned = re.split(r'[,(]', cleaned)[0].strip()
    # Maximal 50 Zeichen
    return cleaned[:50].strip()

def main():
    initDB()

    with open('/app/recipes_imported.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)

    print(f"Lade {len(recipes)} Rezepte...")
    success = 0
    skipped = 0

    for recipe in recipes:
        name = recipe.get("Name", "").strip()
        description = recipe.get("Description", "").strip()
        rawIngredients = recipe.get("Ingredients", [])

        if not name:
            continue

        try:
            rid = addRecipe(name, description)
        except Exception as e:
            skipped += 1
            continue

        for rawIng in rawIngredients:
            ingName = extractIngredientName(rawIng)
            if not ingName:
                continue
            try:
                zid = getOrCreateIngredient(ingName)
                addIngredientToRecipe(zid, rid, 1.0)
            except Exception:
                pass

        success += 1
        if success % 50 == 0:
            print(f"  {success} Rezepte verarbeitet...")

    print(f"Fertig! {success} Rezepte importiert, {skipped} übersprungen.")

if __name__ == "__main__":
    main()