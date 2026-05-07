import sqlite3
from contextlib import contextmanager
from pathlib import Path
import os

# Verwende die Datenbank aus dem data-Ordner
DB_PATH = Path(__file__).parent.parent / "data" / "LazyCookDB.sqlite3"

# Stelle sicher, dass das Verzeichnis existiert
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def getConnection() -> sqlite3.Connection:
    """Erstellt eine neue SQLite-Connection mit Row-Factory."""
    con = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    # con.execute("PRAGMA journal_mode = WAL")
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

        # Refresh Tokens – pro Account können mehrere existieren (z.B. verschiedene Geräte)
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
                    CREATE TABLE IF NOT EXISTS Ingridient (
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
                                                          vid INTEGER NOT NULL,
                                                          FOREIGN KEY (vid) REFERENCES Author (id) ON DELETE CASCADE
                        )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Exists_from (
                                                               zid INTEGER NOT NULL,
                                                               rid INTEGER NOT NULL,
                                                               amount DECIMAL(10,2) NOT NULL,
                        FOREIGN KEY (zid) REFERENCES Ingridient (id) ON DELETE CASCADE,
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

    print("✅ Datenbank-Tabellen erfolgreich initialisiert")


# ── Account-Operationen ──────────────────────────────────────────


def createAccount(email: str, name: str, hashedPassword: str) -> dict | None:
    """Legt ein neues Account an. Gibt die Account-Daten zurück oder None bei Duplikat."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("SELECT 1 FROM Account WHERE email = ? LIMIT 1", (email,))
        if cur.fetchone():
            return None
        cur.execute(
            "INSERT INTO Account (email, name, hashedPassword) VALUES (?, ?, ?)",
            (email, name, hashedPassword),
        )
        return {"id": cur.lastrowid, "email": email, "name": name}


def getAccountByEmail(email: str) -> dict | None:
    """Gibt Account-Daten inkl. hashedPassword zurück, oder None."""
    con = getConnection()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT id, email, name, hashedPassword FROM Account WHERE email = ?",
            (email,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        con.close()


# ── Refresh-Token-Operationen ──────────────────────────────────


def saveRefreshToken(AccountID: int, token: str, expiresAt: str) -> None:
    """Speichert einen neuen Refresh Token in der Datenbank."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO RefreshToken (AccountID, token, expiresAt) VALUES (?, ?, ?)",
            (AccountID, token, expiresAt),
        )


def getRefreshToken(token: str) -> dict | None:
    """Gibt den Refresh-Token-Eintrag zurück, oder None."""
    con = getConnection()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT rt.id, rt.AccountID, rt.token, rt.expiresAt, k.email, k.name "
            "FROM RefreshToken rt JOIN Account k ON rt.AccountID = k.id "
            "WHERE rt.token = ?",
            (token,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        con.close()


def deleteRefreshToken(token: str) -> None:
    """Löscht einen einzelnen Refresh Token (Logout)."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM RefreshToken WHERE token = ?", (token,))


def deleteAllRefreshTokens(AccountID: int) -> None:
    """Löscht alle Refresh Tokens eines Accounts (Logout von allen Geräten)."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM RefreshToken WHERE AccountID = ?", (AccountID,))


def deleteAccount(email: str) -> bool:
    """Löscht ein Account anhand der E-Mail. Refresh Tokens werden via CASCADE mitgelöscht."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM Account WHERE email = ?", (email,))
        return cur.rowcount > 0


def updateAccount(konto_id: int, email: str = None, password_hash: str = None) -> None:
    """Aktualisiert E-Mail und/oder Passwort eines Accounts."""
    with getDB() as con:
        cur = con.cursor()
        if email:
            cur.execute("UPDATE Account SET email = ? WHERE id = ?", (email, konto_id))
        if password_hash:
            cur.execute(
                "UPDATE Account SET hashedPassword = ? WHERE id = ?",
                (password_hash, konto_id),
            )


def cleanupExpiredTokens() -> None:
    """Löscht alle abgelaufenen Refresh Tokens."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM RefreshToken WHERE expiresAt < datetime('now')")
