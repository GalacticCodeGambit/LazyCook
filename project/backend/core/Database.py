"""
Database.py – SQLite-Verbindungsmanagement und Tabellen-Initialisierung
"""

import sqlite3
import logging
from contextlib import contextmanager
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent.parent.parent / "data" / "LazyCookDB.sqlite3"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def getConnection() -> sqlite3.Connection:
    """Erstellt eine neue SQLite-Connection mit Row-Factory."""
    con = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


@contextmanager
def getDB():
    """Context-Manager: öffnet Connection, committed bei Erfolg, rollt bei Fehler zurück."""
    con = getConnection()
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def initDB():
    """Erstellt alle Tabellen, falls sie noch nicht existieren."""
    with getDB() as con:
        cur = con.cursor()

        cur.execute("""
                CREATE TABLE IF NOT EXISTS Account (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(250) NOT NULL UNIQUE,
                name TEXT NOT NULL,
                hashedPassword TEXT NOT NULL,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS RefreshToken (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                AccountID INTEGER NOT NULL,
                token TEXT NOT NULL UNIQUE,
                expiresAt TIMESTAMP NOT NULL,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (AccountID) REFERENCES Account (id) ON DELETE CASCADE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Ingredient (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                amountType VARCHAR(30) NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Author (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Recipe (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description nvarchar(20000),
                vid INTEGER,
                FOREIGN KEY (vid) REFERENCES Author (id) ON DELETE CASCADE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Exists_from (
                zid INTEGER NOT NULL,
                rid INTEGER NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (zid) REFERENCES Ingredient (id) ON DELETE CASCADE,
                FOREIGN KEY (rid) REFERENCES Recipe (id) ON DELETE CASCADE,
                UNIQUE (zid, rid)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Favorites (
                AccountID INTEGER NOT NULL,
                rid INTEGER NOT NULL,
                FOREIGN KEY (AccountID) REFERENCES Account (id) ON DELETE CASCADE,
                FOREIGN KEY (rid) REFERENCES Recipe (id) ON DELETE CASCADE,
                UNIQUE (AccountID, rid)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS IngredientUsage (
                AccountID INTEGER NOT NULL,
                name TEXT NOT NULL,
                displayName TEXT NOT NULL,
                count INTEGER NOT NULL DEFAULT 1,
                lastUnit TEXT,
                lastUsedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (AccountID, name),
                FOREIGN KEY (AccountID) REFERENCES Account (id) ON DELETE CASCADE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS PasswordResetToken (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kontoID INTEGER NOT NULL,
                tokenHash TEXT NOT NULL UNIQUE,
                expiresAt TIMESTAMP NOT NULL,
                usedAt TIMESTAMP,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (kontoID) REFERENCES Account (id) ON DELETE CASCADE
            )
        """)

    logger.info("Datenbank-Tabellen erfolgreich initialisiert")
