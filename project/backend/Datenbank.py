from typing import Dict, Any
import sqlite3


class Datenbank:
    def __init__(self):
        self.verbindeDB()

    def verbindeDB(self):
        self.con = sqlite3.connect("LazyCookDB")
        self.con.row_factory = sqlite3.Row
        self.db = self.con.cursor()
        self.db.execute("PRAGMA foreign_keys = ON")
        self.__create_tables_if_not_exist()

    def get_connection(self):
        """Neue Verbindung für jeden Request"""
        con = sqlite3.connect("LazyCookDB", check_same_thread=False)
        con.row_factory = sqlite3.Row
        return con

    def __create_tables_if_not_exist(self):
        try:
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS Zutat (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    mengenArt VARCHAR(30) NOT NULL
                    
                )
            """
            )
            
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS Rezept (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    vid INTEGER NOT NULL,
                    FOREIGN KEY (vid) REFERENCES Verfasser (id) ON DELETE CASCADE
                    
                )
            """
            )
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS Besteht_Aus (
                    zid INTEGER NOT NULL,
                    rid INTEGER NOT NULL,
                    menge DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (zid) REFERENCES Zutat (id) ON DELETE CASCADE,
                    FOREIGN KEY (rid) REFERENCES Rezept (id) ON DELETE CASCADE,
                    UNIQUE (zid, rid)
                    
                )
            """
            )
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS Verfasser (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                    
                )
            """
            )
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS Nutzer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    kid INTEGER NOT NULL,
                    FOREIGN KEY (kid) REFERENCES Konto (id) ON DELETE CASCADE
                )
            """
            )
 
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS Besteht_Aus (
                    nid INTEGER NOT NULL,
                    rid INTEGER NOT NULL,
                    FOREIGN KEY (nid) REFERENCES Zutat (id) ON DELETE CASCADE,
                    FOREIGN KEY (rid) REFERENCES Rezept (id) ON DELETE CASCADE,
                    UNIQUE (nid, rid)
                    
                )
            """
            )
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS Konto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email VARCHAR(250) NOT NULL UNIQUE,
                    passwort TEXT NOT NULL,
                    salt TEXT NOT NULL
                )
            """
            )
            self.con.commit()
            print("✅ Datenbank-Tabellen erfolgreich initialisiert")
        except Exception as e:
            print(f"Fehler bei Tabellenerstellung: {e}")
            self.con.rollback()

    def addNutzer(self, email, salt, passwort):
        con = self.get_connection()

        db = con.cursor()
        db.execute("""
                SELECT email FROM KONTO
            """
        )
        ergebnis=db.fetchall()
        for row in ergebnis:
            if row["email"]==email:
                return "Email schon in einem Konto registriert"
        db.execute(
                "INSERT INTO KONTO (email, passwort, salt) VALUES (?, ?, ?)",
            (email, passwort, salt),
        )
        db.execute(
                "SELECT id FROM KONTO WHERE email = ?",
                (email,),
        )
        kid=db.fetchone()
        db.execute(
                "INSERT INTO Nutzer (kid) VALUES (?)",
            (kid["id"],),
        )
        con.commit()
        return "Registrierung erfolgreich"

    def anmeldenNutzer(self, email):
        con = self.get_connection()

        db = con.cursor()

        db.execute(
                "SELECT passwort, salt FROM KONTO WHERE email = ?",
                (email,),
        )
        row=db.fetchone()
        if row is None:
            return None
        else:

            return row
        
    def speichernInDB(self, daten: Dict[str, Any]):
        pass

    def holeDaten(self, tabelle: str) -> list[Dict[str, Any]]:
        pass
    def entferneTextSyntax(self, text):
        text = (
            text.replace("(", "")
            .replace(")", "")
            .replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace(",", "")
        )
        return text
    def close(self):
        self.con.close()

        """Alles Nachfolgende sind Testfunktionen
        """
    def test_anmelden(self):
        print("===== Starte Test: anmeldenNutzer() =====")

        # 1. Testnutzer anlegen
        email = "test@example.com"
        name = "Testuser"
        pw = "meinpasswort"

        print("Lege Testnutzer an...")
        self.addNutzer(email, name, pw)

        # 2. Fall 1: richtige Daten
        print("\nTest 1: korrekte Anmeldung")
        result = self.anmeldenNutzer(email, pw)
        print("Erwartet: Anmeldung erfolgreich  |   Ergebnis:", result)

        # 3. Fall 2: falsches Passwort
        print("\nTest 2: falsches Passwort")
        result = self.anmeldenNutzer(email, "falsch123")
        print("Erwartet: Passwort ist falsch!   |   Ergebnis:", result)

        # 4. Fall 3: Email existiert nicht
        print("\nTest 3: Email existiert nicht")
        result = self.anmeldenNutzer("nichtda@test.de", pw)
        print("Erwartet: Email nicht gefunden!  |   Ergebnis:", result)

        print("\n===== Test abgeschlossen =====")




    def test_print_tables(self):
        try:
            cursor = self.con.cursor()

            # Alle Tabellennamen holen
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%';
            """)
            tables = cursor.fetchall()

            if not tables:
                print("Keine Tabellen gefunden.")
                return

            for (table_name,) in tables:
                print(f"\n===== Tabelle: {table_name} =====")

                # Spalteninformationen abfragen
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()

                if columns:
                    print("Spalten:")
                    for col in columns:
                        cid, name, col_type, notnull, dflt_value, pk = col
                        print(f"  - {name} ({col_type})"
                            f"{' NOT NULL' if notnull else ''}"
                            f"{' [PK]' if pk else ''}"
                            f"{f' DEFAULT {dflt_value}' if dflt_value is not None else ''}")
                else:
                    print("  Keine Spalten gefunden (seltsam).")

                # Foreign Keys anzeigen
                cursor.execute(f"PRAGMA foreign_key_list({table_name});")
                fks = cursor.fetchall()
                if fks:
                    print("Foreign Keys:")
                    for fk in fks:
                        id, seq, table, from_col, to_col, on_update, on_delete, match = fk
                        print(f"  - {from_col} -> {table}({to_col}) ON DELETE {on_delete}")
                else:
                    print("Keine Foreign Keys.")

        except Exception as e:
            print(f"Fehler beim Testen der Tabellen: {e}")


