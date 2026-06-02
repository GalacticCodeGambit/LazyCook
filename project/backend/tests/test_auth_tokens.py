import pytest
import sys
import os
from datetime import timedelta, timezone, datetime
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import Database
from Auth import (
    createAccessToken,
    decodeToken,
    hashResetToken,
    createPasswordResetToken,
    validatePasswordResetToken,
    createRefreshToken,
    validateRefreshToken,
)


class TestAccessToken:
    def testTokenErstellen(self):
        token = createAccessToken({"sub": "test@example.com"})
        assert isinstance(token, str)
        assert len(token) > 0

    def testTokenDekodieren(self):
        token = createAccessToken({"sub": "test@example.com"})
        email = decodeToken(token)
        assert email == "test@example.com"

    def testAbgelaufenerToken(self):
        token = createAccessToken({"sub": "test@example.com"}, expires_delta=timedelta(seconds=-1))
        assert decodeToken(token) is None

    def testUngueltigerToken(self):
        assert decodeToken("das.ist.kein.token") is None

    def testLeeresSubject(self):
        token = createAccessToken({})
        assert decodeToken(token) is None


class TestHashResetToken:
    def testHashIstDeterministisch(self):
        assert hashResetToken("abc") == hashResetToken("abc")

    def testHashIstVerschieden(self):
        assert hashResetToken("abc") != hashResetToken("xyz")

    def testHashLaenge(self):
        assert len(hashResetToken("test")) == 64  # SHA-256 hex


class TestPasswordResetToken:
    def testTokenErstellen(self):
        with patch.object(Database, "savePasswordResetToken") as mockSave:
            token = createPasswordResetToken(42)
            assert isinstance(token, str)
            mockSave.assert_called_once()
            assert mockSave.call_args[0][0] == 42

    def testGueltigerToken(self):
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        mockEntry = {"id": 1, "kontoID": 42, "expiresAt": expires, "usedAt": None}
        with patch.object(Database, "getPasswordResetToken", return_value=mockEntry):
            result = validatePasswordResetToken("irgendeintoken")
            assert result is not None
            assert result["kontoID"] == 42

    def testUngueltigerToken(self):
        with patch.object(Database, "getPasswordResetToken", return_value=None):
            assert validatePasswordResetToken("nichtvorhanden") is None

    def testBereitsVerwendeterToken(self):
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        mockEntry = {"id": 1, "kontoID": 42, "expiresAt": expires, "usedAt": "2024-01-01"}
        with patch.object(Database, "getPasswordResetToken", return_value=mockEntry):
            assert validatePasswordResetToken("token") is None

    def testAbgelaufenerResetToken(self):
        expires = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        mockEntry = {"id": 1, "kontoID": 42, "expiresAt": expires, "usedAt": None}
        with patch.object(Database, "getPasswordResetToken", return_value=mockEntry):
            assert validatePasswordResetToken("token") is None


class TestRefreshToken:
    def testRefreshTokenErstellen(self):
        with patch("Auth.saveRefreshToken") as mockSave:
            token = createRefreshToken(99)
            assert isinstance(token, str)
            mockSave.assert_called_once()
            assert mockSave.call_args[0][0] == 99

    def testGueltigerRefreshToken(self):
        expires = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
        mockEntry = {"id": 1, "AccountID": 99, "token": "abc", "expiresAt": expires}
        with patch("Auth.getRefreshToken", return_value=mockEntry):
            result = validateRefreshToken("abc")
            assert result is not None
            assert result["AccountID"] == 99

    def testUngueltigerRefreshToken(self):
        with patch("Auth.getRefreshToken", return_value=None):
            assert validateRefreshToken("ungueltig") is None

    def testAbgelaufenerRefreshToken(self):
        expires = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        mockEntry = {"id": 1, "AccountID": 99, "token": "alt", "expiresAt": expires}
        with patch("Auth.getRefreshToken", return_value=mockEntry):
            assert validateRefreshToken("alt") is None
