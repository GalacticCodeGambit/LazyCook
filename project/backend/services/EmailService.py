import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

gmailUser = os.environ.get("GMAIL_USER")
gmailPassword = os.environ.get("GMAIL_PASSWORD")


def _sendMail(to: str, subject: str, html: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmailUser
    msg["To"] = to
    msg.attach(MIMEText(html, "html"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmailUser, gmailPassword)
        server.sendmail(gmailUser, to, msg.as_string())


def sendPasswordChangedEmail(to_email: str, name: str) -> None:
    html = f"""
        <div style="font-family: sans-serif; max-width: 500px; margin: auto;">
            <h2>Hallo {name},</h2>
            <p>dein Passwort bei <strong>Lazy Cook</strong> wurde soeben geändert.</p>
            <p>Falls du das nicht warst, kontaktiere uns sofort.</p>
            <br>
            <p>– Das Lazy Cook Team</p>
        </div>
    """
    try:
        _sendMail(to_email, "Dein Passwort wurde geändert", html)
    except Exception as e:
        logger.error("Passwort-Änderungs-Mail konnte nicht gesendet werden: %s", e)
        raise


def sendPasswordResetEmail(to_email: str, name: str, resetLink: str) -> None:
    html = f"""
        <div style="font-family: sans-serif; max-width: 500px; margin: auto;">
            <h2>Hallo {name},</h2>
            <p>du hast angefordert, dein Passwort bei <strong>Lazy Cook</strong> zurückzusetzen.</p>
            <p>Klicke auf den Button, um ein neues Passwort festzulegen:</p>
            <p style="text-align:center; margin: 24px 0;">
                <a href="{resetLink}"
                   style="background:#030213; color:#fff; padding:12px 24px;
                          text-decoration:none; border-radius:6px; display:inline-block;">
                    Passwort zurücksetzen
                </a>
            </p>
            <p style="font-size:12px; color:#666;">
                Oder kopiere diesen Link in deinen Browser:<br>
                <a href="{resetLink}">{resetLink}</a>
            </p>
            <p>Der Link ist <strong>30 Minuten</strong> gültig.</p>
            <p>Falls du das nicht angefordert hast, ignoriere diese E-Mail einfach – dein Passwort bleibt unverändert.</p>
            <br>
            <p>– Das Lazy Cook Team</p>
        </div>
    """
    try:
        _sendMail(to_email, "Passwort zurücksetzen – Lazy Cook", html)
    except Exception as e:
        logger.error("Reset-Mail konnte nicht gesendet werden: %s", e)
        raise
