import pytest
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Auth import validatePassword, hashPassword, verifyPassword

class TestValidatePassword:
    def testGueltigesPasswort(self):
        assert validatePassword("Sicher1!") is None

    def testZuKurz(self):
        assert validatePassword("Ab1!") is not None

    def testKeinGrossbuchstabe(self):
        assert validatePassword("sicher1!") is not None

    def testKeinKleinbuchstabe(self):
        assert validatePassword("SICHER1!") is not None

    def testKeineZahl(self):
        assert validatePassword("SicherAB!") is not None

    def testKeinSonderzeichen(self):
        assert validatePassword("Sicher123") is not None


class TestPasswortHashing:
    def testHashIstVerschieden(self):
        hashed = hashPassword("Sicher1!")
        assert hashed != "Sicher1!"

    def testVerifyKorrektesPasswort(self):
        hashed = hashPassword("Sicher1!")
        assert verifyPassword("Sicher1!", hashed) is True

    def testVerifyFalschesPasswort(self):
        hashed = hashPassword("Sicher1!")
        assert verifyPassword("Falsch1!", hashed) is False