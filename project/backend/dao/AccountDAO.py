"""
account_dao.py – Data Access Object für Account, RefreshToken und PasswordResetToken
"""
from core.Database import getDB, getConnection


# ── Account ──────────────────────────────────────────────────────


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


def getAccountById(konto_id: int) -> dict | None:
    """Gibt Account-Daten anhand der ID zurück, oder None."""
    con = getConnection()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT id, email, name, hashedPassword FROM Account WHERE id = ?",
            (konto_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        con.close()


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


def updateKontoPassword(konto_id: int, hashed_password: str) -> None:
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE Account SET hashedPassword = ? WHERE id = ?",
            (hashed_password, konto_id),
        )


def deleteAccount(email: str) -> bool:
    """Löscht ein Account anhand der E-Mail. Refresh Tokens werden via CASCADE mitgelöscht."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM Account WHERE email = ?", (email,))
        return cur.rowcount > 0


# ── Refresh Token ──────────────────────────────────────────────


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
    """Löscht alle Refresh Tokens eines Accounts."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM RefreshToken WHERE AccountID = ?", (AccountID,))


def cleanupExpiredTokens() -> None:
    """Löscht alle abgelaufenen Refresh Tokens."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM RefreshToken WHERE expiresAt < datetime('now')")


# ── Password Reset Token ───────────────────────────────────────


def savePasswordResetToken(kontoID: int, tokenHash: str, expiresAt: str) -> None:
    """Invalidiert alte Tokens des Kontos und speichert einen neuen."""
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE PasswordResetToken SET usedAt = CURRENT_TIMESTAMP "
            "WHERE kontoID = ? AND usedAt IS NULL",
            (kontoID,),
        )
        cur.execute(
            "INSERT INTO PasswordResetToken (kontoID, tokenHash, expiresAt) VALUES (?, ?, ?)",
            (kontoID, tokenHash, expiresAt),
        )


def getPasswordResetToken(tokenHash: str) -> dict | None:
    con = getConnection()
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT id, kontoID, tokenHash, expiresAt, usedAt "
            "FROM PasswordResetToken WHERE tokenHash = ?",
            (tokenHash,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        con.close()


def markResetTokenUsed(tokenID: int) -> None:
    with getDB() as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE PasswordResetToken SET usedAt = CURRENT_TIMESTAMP WHERE id = ?",
            (tokenID,),
        )
