from Datenbank import Datenbank
from models import UserSignUpIn
from passlib.context import CryptContext
import hashlib
import base64
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Dein Frontend Port
    allow_credentials=True,
    allow_methods=["*"],  # Erlaubt alle Methoden (GET, POST, etc.)
    allow_headers=["*"],  # Erlaubt alle Headers
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

datenbank = Datenbank()

def hash_password(password: str) -> tuple[str, str]:
    # 16-Byte zufälliges Salt erzeugen
    salt = os.urandom(16)

    # PBKDF2-HMAC mit SHA256
    key = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=100_000
    )

    # Base64 für Speicherung
    return base64.b64encode(salt).decode(), base64.b64encode(key).decode()

def verify_password(password: str, salt_b64: str, key_b64: str) -> bool:
    """
    Validate a plaintext password against a stored salt and derived key.
    
    Parameters:
        password (str): The plaintext password to verify.
        salt_b64 (str): Base64-encoded salt used when the stored key was derived.
        key_b64 (str): Base64-encoded derived key (password hash) to compare against.
    
    Returns:
        bool: `True` if the password, when derived with the provided salt, matches the stored key; `False` otherwise.
    """
    salt = base64.b64decode(salt_b64)
    key_original = base64.b64decode(key_b64)

    key_check = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=100_000
    )

    return key_check == key_original

# TODO: production error messages generalisieren - issue #90
@app.post("/api/login")
def anmelden(user: UserSignUpIn):

    """
    Authenticate a user by email and password.
    
    Parameters:
        user (UserSignUpIn): Object containing `email` and `password` for authentication.
    
    Returns:
        dict: A dictionary with a single `"message"` key describing the outcome:
            - "Anmeldung erfolgreich" if authentication succeeds.
            - "Falsches Passwort" if the password is incorrect.
            - "Für diese Email ist kein Konto hinterlegt" if no account exists for the provided email.
            - "Anmeldung fehlgeschlagen" if an unexpected error occurs.
    """
    try:
        row = datenbank.anmeldenNutzer(user.email)

        if row is None:
            return {
                "message": "Für diese Email ist kein Konto hinterlegt"
            }

        key = row["passwort"]
        salt = row["salt"]

        correct = verify_password(user.password, salt, key)

        if correct:
            return {
                "message": "Anmeldung erfolgreich"
            }
        else:
            return {
                "message": "Falsches Passwort"
            }


    except Exception as e:
        return {
            "message": "Anmeldung fehlgeschlagen"
        }


@app.post("/api/register")
async def registrieren(user: UserSignUpIn):

    salt, password = hash_password(user.password)

    try:
        message = datenbank.addNutzer(user.email, salt, password)
    except Exception as e:
        return {
            "message": "Registrierung fehlgeschlagen"
        }

    return {
            "message": message
    }


def filternNachZutat(self, anzPersonen: int, zutaten_liste: list[str]):
    pass

def suchenNachRezept(self, name: str):
   pass

def zeigeRezepteAn(self):
   pass



