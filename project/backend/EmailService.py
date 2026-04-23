import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

def sendPasswordChangedEmail(to_email: str, name: str) -> None:
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Dein Passwort wurde geändert"
        msg["From"] = GMAIL_USER
        msg["To"] = to_email

        html = f"""
            <div style="font-family: sans-serif; max-width: 500px; margin: auto;">
                <h2>Hallo {name},</h2>
                <p>dein Passwort bei <strong>Lazy Cook</strong> wurde soeben geändert.</p>
                <p>Falls du das nicht warst, kontaktiere uns sofort.</p>
                <br>
                <p>– Das Lazy Cook Team</p>
            </div>
        """
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())

    except Exception as e:
        print(f"E-Mail Fehler: {e}")
        raise