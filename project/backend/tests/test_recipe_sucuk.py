import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import services.RecipeSUCUK as recipe_service_module
from domain.ingredient import Ingredient
from services.RecipeSUCUK import findRecipes


# ── Hilfsfunktionen ────────────────────────────────────────────

def makeRawRecipe(id: int, name: str, description: str = "") -> dict:
    return {"id": id, "name": name, "description": description}

def makeIngredients(names: list[str]) -> list[Ingredient]:
    return [Ingredient(name, 1.0) for name in names]

def mockIngredientsByRecipeId(mapping: dict):
    return lambda rid: mapping.get(rid, [])

def runFindRecipes(rawRecipes, ingredientMapping, searchIngredients, index=0):
    """Patcht beide DAO-Aufrufe und ruft findRecipes auf."""
    with patch.object(recipe_service_module.RecipeDAO, "getAllRecipes", return_value=rawRecipes), \
         patch.object(recipe_service_module.IngredientDAO, "getIngredientsForRecipe",
                      side_effect=mockIngredientsByRecipeId(ingredientMapping)):
        return findRecipes(searchIngredients, index)


# ── Tests ──────────────────────────────────────────────────────

class TestFindRecipesKeinTreffer:
    def testLeereDB(self):
        result = runFindRecipes([], {}, [Ingredient("Mehl", 1)])
        assert result == []

    def testKeineUebereinstimmung(self):
        raw = [makeRawRecipe(1, "Pasta")]
        ing = {1: makeIngredients(["Nudeln"])}
        result = runFindRecipes(raw, ing, [Ingredient("Mehl", 1)])
        assert len(result) == 1
        assert result[0].getRating() == 0.0

    def testLeereZutatenliste(self):
        raw = [makeRawRecipe(1, "Pasta"), makeRawRecipe(2, "Pizza")]
        ing = {1: makeIngredients(["Nudeln"]), 2: makeIngredients(["Teig"])}
        result = runFindRecipes(raw, ing, [])
        assert len(result) == 2


class TestFindRecipesTreffer:
    def testEinTreffer(self):
        raw = [makeRawRecipe(1, "Pasta")]
        ing = {1: makeIngredients(["Nudeln", "Salz"])}
        result = runFindRecipes(raw, ing, [Ingredient("Nudeln", 1)])
        assert len(result) == 1
        assert result[0].getName() == "Pasta"
        assert result[0].getRating() == 0.5  # 1 von 2 Zutaten

    def testMehrereTrefferSortierungNachRating(self):
        raw = [makeRawRecipe(1, "Pasta"), makeRawRecipe(2, "Pizza")]
        ing = {
            1: makeIngredients(["Nudeln", "Salz"]),
            2: makeIngredients(["Teig"]),
        }
        result = runFindRecipes(raw, ing, [Ingredient("Nudeln", 1), Ingredient("Teig", 1)])
        assert result[0].getName() == "Pizza"  # Rating 1.0
        assert result[1].getName() == "Pasta"  # Rating 0.5

    def testRatingBerechnung(self):
        raw = [makeRawRecipe(1, "Pasta")]
        ing = {1: makeIngredients(["A", "B", "C"])}
        result = runFindRecipes(raw, ing, [Ingredient("A", 1), Ingredient("B", 1)])
        assert round(result[0].getRating(), 4) == round(2 / 3, 4)

    def testAlleZutatenTreffen(self):
        raw = [makeRawRecipe(1, "Pasta")]
        ing = {1: makeIngredients(["Nudeln", "Salz"])}
        result = runFindRecipes(raw, ing, [Ingredient("Nudeln", 1), Ingredient("Salz", 1)])
        assert result[0].getRating() == 1.0


class TestFindRecipesPaginierung:
    def _buildRecipes(self, n: int):
        raw = [makeRawRecipe(i, f"Rezept{i}") for i in range(n)]
        ing = {i: makeIngredients([f"Zutat{i}"]) for i in range(n)}
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
