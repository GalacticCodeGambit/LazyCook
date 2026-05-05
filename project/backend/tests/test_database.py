import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import Database
from Auth import hashPassword, verifyPassword
from Database import createAccount, getAccountByEmail, deleteAccount, updateAccount


@pytest.fixture(autouse=True)
def useTestDb():
    Database.initDB()
    yield
    # Tabellen nach jedem Test leeren
    con = Database.getConnection()
    con.execute("DELETE FROM Account")
    con.commit()
    con.close()


class TestCreateAccount:
    def testAccountErstellen(self):
        result = createAccount("test@example.com", "Test User", "hashedPW")
        assert result is not None
        assert result["email"] == "test@example.com"

    def testDuplikatEmail(self):
        createAccount("test@example.com", "Test User", "hashedPW")
        result = createAccount("test@example.com", "Anderer User", "hashedPW")
        assert result is None


class TestGetAccountByEmail:
    def testAccountGefunden(self):
        createAccount("test@example.com", "Test User", "hashedPW")
        account = getAccountByEmail("test@example.com")
        assert account is not None
        assert account["email"] == "test@example.com"

    def testAccountNichtGefunden(self):
        result = getAccountByEmail("nichtvorhanden@example.com")
        assert result is None


class TestDeleteAccount:
    def testAccountLoeschen(self):
        createAccount("test@example.com", "Test User", "hashedPW")
        result = deleteAccount("test@example.com")
        assert result is True
        assert getAccountByEmail("test@example.com") is None

    def testNichtVorhandenenAccountLoeschen(self):
        result = deleteAccount("nichtvorhanden@example.com")
        assert result is False


class TestUpdateAccount:
    def testEmailAendern(self):
        account = createAccount("alt@example.com", "Test User", "hashedPW")
        updateAccount(account["id"], email="neu@example.com")
        assert getAccountByEmail("neu@example.com") is not None
        assert getAccountByEmail("alt@example.com") is None

    def testPasswortAendern(self):
        account = createAccount("test@example.com", "Test User", hashPassword("Alt1!"))
        neuerHash = hashPassword("Neu1!")
        updateAccount(account["id"], password_hash=neuerHash)
        aktuell = getAccountByEmail("test@example.com")
        # Note: The Database has 'hashedPassword' column
        assert verifyPassword("Neu1!", aktuell["hashedPassword"]) is True
