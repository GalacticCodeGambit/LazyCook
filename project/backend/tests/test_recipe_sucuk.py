import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import RecipeSucuk
import Ingredient as IngredientModule
from Ingredient import Ingredient
from RecipeSucuk import findRecipes


# ── Hilfsfunktionen ────────────────────────────────────────────

def makeRawRecipe(id: int, name: str, description: str = "") -> dict:
    return {"id": id, "name": name, "description": description}

def makeRawIngredient(name: str, amount: float = 1.0) -> dict:
    return {"name": name, "amount": amount, "amountType": "g"}

def mockIngredients(mapping: dict):
    return lambda rid: mapping.get(rid, [])

def runFindRecipes(rawRecipes, ingredientMapping, searchIngredients, index=0):
    """Hilfsfunktion: patcht beide DB-Aufrufe und ruft findRecipes auf."""
    with patch.object(RecipeSucuk, "getAllRecipes", return_value=rawRecipes), \
         patch.object(IngredientModule, "getAllIngredientsForRecipe",
                      side_effect=mockIngredients(ingredientMapping)):
        return findRecipes(searchIngredients, index)


# ── Tests ──────────────────────────────────────────────────────

class TestFindRecipesKeinTreffer:
    def testLeereDB(self):
        result = runFindRecipes([], {}, [Ingredient("Mehl", 1)])
        assert result == []

    def testKeineUebereinstimmung(self):
        raw = [makeRawRecipe(1, "Pasta")]
        ing = {1: [makeRawIngredient("Nudeln")]}
        result = runFindRecipes(raw, ing, [Ingredient("Mehl", 1)])
        assert len(result) == 1
        assert result[0].getRating() == 0.0

    def testLeereZutatenliste(self):
        raw = [makeRawRecipe(1, "Pasta"), makeRawRecipe(2, "Pizza")]
        ing = {1: [makeRawIngredient("Nudeln")], 2: [makeRawIngredient("Teig")]}
        result = runFindRecipes(raw, ing, [])
        assert len(result) == 2


class TestFindRecipesTreffer:
    def testEinTreffer(self):
        raw = [makeRawRecipe(1, "Pasta")]
        ing = {1: [makeRawIngredient("Nudeln"), makeRawIngredient("Salz")]}
        result = runFindRecipes(raw, ing, [Ingredient("Nudeln", 1)])
        assert len(result) == 1
        assert result[0].getName() == "Pasta"
        assert result[0].getRating() == 0.5  # 1 von 2 Zutaten

    def testMehrereTrefferSortierungNachRating(self):
        raw = [makeRawRecipe(1, "Pasta"), makeRawRecipe(2, "Pizza")]
        ing = {
            1: [makeRawIngredient("Nudeln"), makeRawIngredient("Salz")],
            2: [makeRawIngredient("Teig")],
        }
        # Nudeln trifft Pasta (1/2 = 0.5), Teig trifft Pizza (1/1 = 1.0)
        result = runFindRecipes(raw, ing, [Ingredient("Nudeln", 1), Ingredient("Teig", 1)])
        assert result[0].getName() == "Pizza"  # Rating 1.0
        assert result[1].getName() == "Pasta"  # Rating 0.5

    def testRatingBerechnung(self):
        raw = [makeRawRecipe(1, "Pasta")]
        ing = {1: [makeRawIngredient("A"), makeRawIngredient("B"), makeRawIngredient("C")]}
        result = runFindRecipes(raw, ing, [Ingredient("A", 1), Ingredient("B", 1)])
        assert round(result[0].getRating(), 4) == round(2 / 3, 4)  # 2 von 3 Zutaten

    def testAlleZutatenTreffen(self):
        raw = [makeRawRecipe(1, "Pasta")]
        ing = {1: [makeRawIngredient("Nudeln"), makeRawIngredient("Salz")]}
        result = runFindRecipes(raw, ing, [Ingredient("Nudeln", 1), Ingredient("Salz", 1)])
        assert result[0].getRating() == 1.0


class TestFindRecipesPaginierung:
    def _buildRecipes(self, n: int):
        raw = [makeRawRecipe(i, f"Rezept{i}") for i in range(n)]
        ing = {i: [makeRawIngredient(f"Zutat{i}")] for i in range(n)}
        return raw, ing

    def testErsteSeite(self):
        raw, ing = self._buildRecipes(15)
        assert len(runFindRecipes(raw, ing, [])) == 12

    def testZweiteSeite(self):
        raw, ing = self._buildRecipes(15)
        assert len(runFindRecipes(raw, ing, [], index=1)) == 3

    def testLeereSeite(self):
        raw, ing = self._buildRecipes(5)
        assert runFindRecipes(raw, ing, [], index=1) == []

    def testGenauZwoelfRezepte(self):
        raw, ing = self._buildRecipes(12)
        assert len(runFindRecipes(raw, ing, [], index=0)) == 12
        assert runFindRecipes(raw, ing, [], index=1) == []
