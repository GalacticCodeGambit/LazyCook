"""
Test Runner - Führe alle Tests aus
Nutzt pytest zum Sammeln und Ausführen aller Tests im tests-Ordner
"""
import pytest
import sys
import os

if __name__ == "__main__":
    # Suche alle Test-Dateien im aktuellen Verzeichnis und führe sie aus
    pytest.main([
        os.path.dirname(__file__),
        "-v",
        "--tb=short"
    ])
