import pytest
import sys
import os
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import core.Database as Database
from core.Auth import hashPassword, verifyPassword
from dao.AccountDAO import (
    createAccount, getAccountByEmail, deleteAccount, updateAccount,
    getAccountById, saveRefreshToken, getRefreshToken, deleteRefreshToken,
    deleteAllRefreshTokens, cleanupExpiredTokens, savePasswordResetToken,
    getPasswordResetToken, markResetTokenUsed, updateKontoPassword,
)
from dao.RecipeDAO import (
    addRecipe, addIngredientToRecipe, getAllRecipes, getAllIngredientsForRecipe,
)
from dao.IngredientDAO import (
    addIngredient, getIngredientByName, incrementIngredientUsage, getTopIngredients,
)


@pytest.fixture(autouse=True)
def isolatedDb(tmp_path, monkeypatch):
    monkeypatch.setattr(Database, "DB_PATH", tmp_path / "test.db")
    Database.initDB()


@pytest.fixture
def account():
    return createAccount("test@example.com", "Test User", "hashedPW")


# ── Account ────────────────────────────────────────────────────


class TestCreateAccount:
    def testAccountErstellen(self):
        result = createAccount("test@example.com", "Test User", "hashedPW")
        assert result is not None
        assert result["email"] == "test@example.com"

    def testAccountGibtIdZurueck(self):
        result = createAccount("test@example.com", "Test User", "hashedPW")
        assert "id" in result
        assert isinstance(result["id"], int)

    def testAccountGibtNameZurueck(self):
        result = createAccount("test@example.com", "Test User", "hashedPW")
        assert result["name"] == "Test User"

    def testDuplikatEmail(self):
        createAccount("test@example.com", "Test User", "hashedPW")
        result = createAccount("test@example.com", "Anderer User", "hashedPW")
        assert result is None


class TestGetAccountByEmail:
    def testAccountGefunden(self, account):
        result = getAccountByEmail("test@example.com")
        assert result is not None
        assert result["email"] == "test@example.com"

    def testAccountNichtGefunden(self):
        assert getAccountByEmail("nichtvorhanden@example.com") is None


class TestGetAccountById:
    def testAccountGefunden(self, account):
        result = getAccountById(account["id"])
        assert result is not None
        assert result["email"] == "test@example.com"

    def testAccountNichtGefunden(self):
        assert getAccountById(99999) is None


class TestDeleteAccount:
    def testAccountLoeschen(self, account):
        assert deleteAccount("test@example.com") is True
        assert getAccountByEmail("test@example.com") is None

    def testNichtVorhandenenAccountLoeschen(self):
        assert deleteAccount("nichtvorhanden@example.com") is False


class TestUpdateAccount:
    def testEmailAendern(self, account):
        updateAccount(account["id"], email="neu@example.com")
        assert getAccountByEmail("neu@example.com") is not None
        assert getAccountByEmail("test@example.com") is None

    def testPasswortAendern(self, account):
        neuerHash = hashPassword("Neu1!")
        updateAccount(account["id"], password_hash=neuerHash)
        aktuell = getAccountByEmail("test@example.com")
        assert verifyPassword("Neu1!", aktuell["hashedPassword"]) is True


# ── Refresh Token ──────────────────────────────────────────────


class TestRefreshToken:
    def testSpeichernUndAbrufen(self, account):
        expires = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
        saveRefreshToken(account["id"], "token123", expires)
        result = getRefreshToken("token123")
        assert result is not None
        assert result["AccountID"] == account["id"]

    def testNichtVorhandenerToken(self):
        assert getRefreshToken("ungueltig") is None

    def testTokenLoeschen(self, account):
        expires = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
        saveRefreshToken(account["id"], "zuloeschen", expires)
        deleteRefreshToken("zuloeschen")
        assert getRefreshToken("zuloeschen") is None

    def testAlleTokensLoeschen(self, account):
        expires = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
        saveRefreshToken(account["id"], "t1", expires)
        saveRefreshToken(account["id"], "t2", expires)
        deleteAllRefreshTokens(account["id"])
        assert getRefreshToken("t1") is None
        assert getRefreshToken("t2") is None

    def testAbgelaufeneTokensBereinigen(self, account):
        abgelaufen = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        saveRefreshToken(account["id"], "abgelaufen", abgelaufen)
        cleanupExpiredTokens()
        assert getRefreshToken("abgelaufen") is None


# ── Rezept & Zutat ─────────────────────────────────────────────


class TestRezeptUndZutat:
    def testRezeptHinzufuegen(self):
        rid = addRecipe("Testrezept", "Beschreibung", None)
        assert isinstance(rid, int)

    def testZutatHinzufuegen(self):
        zid = addIngredient("Mehl", "g")
        assert isinstance(zid, int)

    def testZutatNachNameSuchen(self):
        addIngredient("Zucker", "g")
        result = getIngredientByName("Zucker")
        assert result is not None
        assert result["amountType"] == "g"

    def testNichtVorhandeneZutatSuchen(self):
        assert getIngredientByName("Nichtvorhanden") is None

    def testZutatZuRezeptVerknuepfen(self):
        rid = addRecipe("Pasta", "Lecker", None)
        zid = addIngredient("Nudeln", "g")
        addIngredientToRecipe(zid, rid, 200.0)
        zutaten = getAllIngredientsForRecipe(rid)
        assert len(zutaten) == 1
        assert zutaten[0]["name"] == "Nudeln"
        assert zutaten[0]["amount"] == 200.0

    def testAlleRezepteAbrufen(self):
        addRecipe("Rezept1", "Beschr1", None)
        addRecipe("Rezept2", "Beschr2", None)
        assert len(getAllRecipes()) == 2

    def testZutatZuRezeptOhneGueltigeIDs(self):
        assert addIngredientToRecipe(None, None, 1.0) is False


# ── Ingredient Usage ───────────────────────────────────────────


class TestIngredientUsage:
    def testNutzungErhoehen(self, account):
        incrementIngredientUsage(account["id"], "Mehl", "g")
        top = getTopIngredients(account["id"])
        assert top[0]["displayName"] == "Mehl"
        assert top[0]["count"] == 1

    def testWiederholteNutzungErhoehen(self, account):
        incrementIngredientUsage(account["id"], "Salz", "g")
        incrementIngredientUsage(account["id"], "Salz", "g")
        assert getTopIngredients(account["id"])[0]["count"] == 2

    def testNormalisierungDesNamens(self, account):
        incrementIngredientUsage(account["id"], "  MEHL  ", "g")
        assert getTopIngredients(account["id"])[0]["displayName"] == "MEHL"

    def testLeererNameWirdIgnoriert(self, account):
        incrementIngredientUsage(account["id"], "", "g")
        assert len(getTopIngredients(account["id"])) == 0

    def testTopIngredientsLimit(self, account):
        for i in range(7):
            incrementIngredientUsage(account["id"], f"Zutat{i}", "g")
        assert len(getTopIngredients(account["id"], limit=5)) == 5


# ── Password Reset ─────────────────────────────────────────────


class TestPasswordReset:
    def testSpeichernUndAbrufen(self, account):
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        savePasswordResetToken(account["id"], "testhash", expires)
        result = getPasswordResetToken("testhash")
        assert result is not None
        assert result["kontoID"] == account["id"]

    def testNichtVorhandenerToken(self):
        assert getPasswordResetToken("nichtvorhanden") is None

    def testAlsVerwendetMarkieren(self, account):
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        savePasswordResetToken(account["id"], "hash456", expires)
        entry = getPasswordResetToken("hash456")
        markResetTokenUsed(entry["id"])
        assert getPasswordResetToken("hash456")["usedAt"] is not None

    def testPasswortAktualisieren(self, account):
        neuerHash = hashPassword("Neu1!")
        updateKontoPassword(account["id"], neuerHash)
        aktuell = getAccountByEmail("test@example.com")
     