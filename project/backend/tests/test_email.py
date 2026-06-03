import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.Auth import validateEmail


class TestValidateEmail:
    def testGueltigeEmail(self):
        assert validateEmail("test@example.com") is None

    def testFehlendesAt(self):
        assert validateEmail("testexample.com") is not None

    def testFehlendeDomain(self):
        assert validateEmail("test@") is not None

    def testLeereEmail(self):
        assert validateEmail("") is not None
