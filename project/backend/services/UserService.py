"""
user_service.py – Geschäftslogik für Account-Verwaltung
"""

import logging

from core.Auth import hashPassword, verifyPassword, validateEmail, validatePassword
from services.EmailService import sendPasswordChangedEmail
from dao import AccountDAO

logger = logging.getLogger(__name__)


def register(email: str, name: str, password: str) -> dict | None:
    """Legt ein neues Konto an. Gibt Account-Dict zurück oder None bei Duplikat."""
    return AccountDAO.createAccount(
        email=email,
        name=name,
        hashedPassword=hashPassword(password),
    )


def updateUser(konto_id: int, current_email: str, data) -> None:
    """Aktualisiert E-Mail und/oder Passwort. Wirft ValueError bei Validierungsfehlern."""
    if data.email:
        error = validateEmail(data.email)
        if error:
            raise ValueError(error)
        AccountDAO.updateAccount(konto_id, email=data.email)

    if data.currentPassword and data.newPassword:
        account = AccountDAO.getAccountById(konto_id)
        if not verifyPassword(data.currentPassword, account["hashedPassword"]):
            raise ValueError("Aktuelles Passwort ist falsch")

        error = validatePassword(data.newPassword)
        if error:
            raise ValueError(error)

        AccountDAO.updateAccount(konto_id, password_hash=hashPassword(data.newPassword))

        receiver_email = data.email if data.email else current_email
        try:
            sendPasswordChangedEmail(receiver_email, account["name"])
        except Exception as e:
            logger.warning("E-Mail konnte nicht gesendet werden: %s", e)
