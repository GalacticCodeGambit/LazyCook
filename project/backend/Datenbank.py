import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path("LazyCookDB.sqlite3")


def get_connection() -> sqlite3.Connection:
    """Erstellt eine neue SQLite-Connection mit Row-Factory."""
    con = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    con.execute("PRAGMA journal_mode = WAL")
    return con


@contextmanager
def get_db():
    """Context-Manager: öffnet Connection, committed bei Erfolg, rollt bei Fehler zurück."""
    con = get_connection()
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def init_db():
    """Erstellt alle Tabellen, falls sie noch nicht existieren."""
    with get_db() as con:
        cur = con.cursor()

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Konto (
                                                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                         email VARCHAR(250) NOT NULL UNIQUE,
                        name TEXT NOT NULL,
                        hashed_password TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)

        # Refresh Tokens – pro Konto können mehrere existieren (z.B. verschiedene Geräte)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS RefreshToken (
                                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                konto_id INTEGER NOT NULL,
                                                                token TEXT NOT NULL UNIQUE,
                                                                expires_at TIMESTAMP NOT NULL,
                                                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                                FOREIGN KEY (konto_id) REFERENCES Konto (id) ON DELETE CASCADE
                        )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Zutat (
                                                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                         name TEXT UNIQUE NOT NULL,
                                                         mengenArt VARCHAR(30) NOT NULL
                        )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Verfasser (
                                                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                             name TEXT UNIQUE NOT NULL
                    )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Rezept (
                                                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          name TEXT UNIQUE NOT NULL,
                                                          vid INTEGER NOT NULL,
                                                          FOREIGN KEY (vid) REFERENCES Verfasser (id) ON DELETE CASCADE
                        )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Besteht_Aus (
                                                               zid INTEGER NOT NULL,
                                                               rid INTEGER NOT NULL,
                                                               menge DECIMAL(10,2) NOT NULL,
                        FOREIGN KEY (zid) REFERENCES Zutat (id) ON DELETE CASCADE,
                        FOREIGN KEY (rid) REFERENCES Rezept (id) ON DELETE CASCADE,
                        UNIQUE (zid, rid)
                        )
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Favoriten (
                                                             konto_id INTEGER NOT NULL,
                                                             rid INTEGER NOT NULL,
                                                             FOREIGN KEY (konto_id) REFERENCES Konto (id) ON DELETE CASCADE,
                        FOREIGN KEY (rid) REFERENCES Rezept (id) ON DELETE CASCADE,
                        UNIQUE (konto_id, rid)
                        )
                    """)

    print("✅ Datenbank-Tabellen erfolgreich initialisiert")


# ── Konto-Operationen ──────────────────────────────────────────

def create_konto(email: str, name: str, hashed_password: str) -> dict | None:
    """Legt ein neues Konto an. Gibt die Konto-Daten zurück oder None bei Duplikat."""
    with get_db() as con:
        cur = con.cursor()
        cur.execute("SELECT 1 FROM Konto WHERE email = ? LIMIT 1", (email,))
        if cur.fetchone():
            return None
        cur.execute(
            "INSERT INTO Konto (email, name, hashed_password) VALUES (?, ?, ?)",
            (email, name, hashed_password),
        )
        return {"id": cur.lastrowid, "email": email, "name": name}


def get_konto_by_email(email: str) -> dict | None:
    """Gibt Konto-Daten inkl. hashed_password zurück, oder None."""
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT id, email, name, hashed_password FROM Konto WHERE email = ?",
            (email,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        con.close()


# ── Refresh-Token-Operationen ──────────────────────────────────

def save_refresh_token(konto_id: int, token: str, expires_at: str) -> None:
    """Speichert einen neuen Refresh Token in der Datenbank."""
    with get_db() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO RefreshToken (konto_id, token, expires_at) VALUES (?, ?, ?)",
            (konto_id, token, expires_at),
        )


def get_refresh_token(token: str) -> dict | None:
    """Gibt den Refresh-Token-Eintrag zurück, oder None."""
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT rt.id, rt.konto_id, rt.token, rt.expires_at, k.email, k.name "
            "FROM RefreshToken rt JOIN Konto k ON rt.konto_id = k.id "
            "WHERE rt.token = ?",
            (token,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        con.close()


def delete_refresh_token(token: str) -> None:
    """Löscht einen einzelnen Refresh Token (Logout)."""
    with get_db() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM RefreshToken WHERE token = ?", (token,))


def delete_all_refresh_tokens(konto_id: int) -> None:
    """Löscht alle Refresh Tokens eines Kontos (Logout von allen Geräten)."""
    with get_db() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM RefreshToken WHERE konto_id = ?", (konto_id,))


def cleanup_expired_tokens() -> None:
    """Löscht alle abgelaufenen Refresh Tokens."""
    with get_db() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM RefreshToken WHERE expires_at < datetime('now')")