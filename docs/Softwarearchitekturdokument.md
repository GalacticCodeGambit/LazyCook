# Einführung und Ziele

## Aufgabenstellung

**Inhalt**

Die Anwendung LazyCook soll Nutzern das Filtern von Rezepten, die den vorhandenen Zutaten entsprechen, ermöglichen. Nutzer sollen Zutaten, Menge und Personenanzahl eingeben können. Rezepte, die auf diese Angaben möglichst genau passen, werden gesucht und angezeigt.

Anforderungen:
- Registrierung und Anmeldung auf der Website
- Abmelden von der Website
- Eingabe von Zutaten, Menge und Personenanzahl
- Entfernen von falschen Eingaben
- Automatisches Suchen und Filtern der Rezepte anhand der Eingaben
- Anzeigen von 12 Rezepten auf einer Seite
- Anzeige von mehr Rezepten bei Bedarf (maximal 96)
- Vorschläge von häufigen Zutaten
- Rezepte auch ohne eingetragenen Zutaten suchen können

Die Anforderungen werden ausführlich im [SRS-Dokument](https://github.com/GalacticCodeGambit/LazyCook/blob/4710a641f177a29e59067edf688781efb3b03a3d/docs/Softwareanforderungsspezifikation%20(SRS).md) aufgeschlüsselt.

**Motivation**

Unsere Nutzer sollen schnell und bequem passende Rezepte zu den Zutaten finden, die sie zu Hause haben. Wir möchten die dafür nötige Anwendung zur Verfügung stellen. Für die einfache Nutzung soll die Anwendung performant, benutzerfreundlich und verfügbar sein.

## Qualitätsziele

**Inhalt**

Die folgenden Qualitätsziele sind für LazyCook maßgeblich und beeinflussen die Architekturentscheidungen:

| Priorität | Qualitätsziel | Beschreibung |
|-----------|---------------|--------------|
| 1 | Effizienz (Zeitverhalten) | Rezepte werden innerhalb von maximal 5 Sekunden nach Klick auf Filtern angezeigt |
| 2 | Sicherheit | Passwörter werden gehasht mit Salt (PBKDF2-HMAC mit SHA256) in der Datenbank gespeichert |
| 3 | Benutzbarkeit | Anmeldung & Registrierung mit möglichst wenigen Klicks; Rezeptvorschläge als 3x3 Matrix |
| 4 | Wartbarkeit (Änderbarkeit) | Neue Features und Bug-Fixes innerhalb von 2 Arbeitstagen umsetzbar |
| 5 | Kompatibilität | Die Anwendung läuft fehlerfrei auf Chrome, Firefox, Safari und Edge |

**Motivation**

Weil Qualitätsziele grundlegende Architekturentscheidungen oft maßgeblich beeinflussen, sollten Sie die für Ihre Stakeholder relevanten Qualitätsziele kennen, möglichst konkret und operationalisierbar.

**Form**

Unser [Qualitätsbaum](https://github.com/GalacticCodeGambit/LazyCook/blob/4710a641f177a29e59067edf688781efb3b03a3d/docs/Qualit%C3%A4tsmerkmale/Qualit%C3%A4tsbaum.md)

Unsere [Qualitätsszenarien](https://github.com/GalacticCodeGambit/LazyCook/blob/4710a641f177a29e59067edf688781efb3b03a3d/docs/Qualit%C3%A4tsmerkmale/Qualit%C3%A4tsszenario.md)

## Stakeholder

| Rolle | Kontakt | Erwartungshaltung |
|-------|---------|-------------------|
| Product-Owner | Samuel Göbel: goebelsamuel@gmail.com | Funktionstüchtige Anwendung entsprechend der gesetzten Anforderungen |
| Kunde/Investor | Harald Ichters: ichters.harald@edu.dhbw-karlsruhe.de | Funktionstüchtige Anwendung mit allen gewünschten Features und den Qualitätsanforderungen. Schnelle Entwicklung |
| Entwickler | Eden Bernhard: etbernhard4@gmail.com, Samuel Göbel, Frederik Behne, Niclas Matzke, Alexander Groer | Klare Anforderungen, direkte Kommunikation, Feedback, Unterstützung im Gesamtprozess, Kommunikation auf Augenhöhe |

---

# Randbedingungen

**Inhalt**

### Technische Randbedingungen

| Randbedingung | Erläuterung |
|---------------|-------------|
| Webbasierte Anwendung | Das Projekt muss als Webanwendung umgesetzt werden |
| Abgabefrist | Das Projekt muss zum Ende des 4. Semesters abgegeben werden |
| Optimierung für Desktop | LazyCook soll für die Benutzung am Laptop oder Computer optimiert sein |
| Docker-Container | Die Anwendung wird mittels Docker Compose containerisiert ausgeliefert |


### Organisatorische Randbedingungen

| Randbedingung | Erläuterung |
|---------------|-------------|
| Team | 5 Entwickler (Eden Bernhard, Niclas Matzke, Frederik Behne, Alexander Groer, Samuel Göbel) |
| Projektmanagement | GitHub Projects zur Aufgabenverwaltung |
| Versionsverwaltung | Git/GitHub |
| CI/CD | GitHub Actions für automatisierte Builds und Tests |

---

# Kontextabgrenzung

**Inhalt**

Unser System ist in sich geschlossen und nur von den verwendeten Technologien abhängig. Die Verwendung einer externen Rezept-API ist noch in Überlegung und wäre dann eine externe Abhängigkeit. Das Frontend kommuniziert über HTTP und JSON mit dem Backend und die Daten werden in einer SQLite-Datenbank gespeichert.

## Fachlicher Kontext

Der Nutzer interagiert mit LazyCook über den Browser. Die fachliche Schnittstelle umfasst folgende Interaktionen:

| Kommunikationspartner | Eingabe | Ausgabe |
|----------------------|---------|---------|
| Nutzer (nicht angemeldet) | Aufruf der Website | Startseite mit Login/Registrierung |
| Nutzer (angemeldet) | E-Mail, Passwort | Bestätigung der Anmeldung, Weiterleitung zum RecipeFinder |
| Nutzer (angemeldet) | Zutaten (Name, Menge, Einheit), Personenanzahl | Passende Rezepte als 3x3 Matrix |
| Nutzer (angemeldet) | Abmelde-Anfrage | Bestätigung, Weiterleitung zur Startseite |

## Technischer Kontext

Die Anwendung besteht aus einem Next.js/React-Frontend, das über eine REST-Schnittstelle mit einem FastAPI-Backend kommuniziert. Das Backend greift auf eine SQLite-Datenbank zur Speicherung von Rezepten und Nutzerdaten zu und kann optional externe Rezept-APIs einbinden. Die Kommunikation erfolgt über HTTP und JSON.

| Technische Schnittstelle | Technologie | Protokoll |
|--------------------------|-------------|-----------|
| Frontend → Backend | REST API | HTTP / JSON |
| Backend → Datenbank | SQLite3 (Python sqlite3-Modul) | Direkte Dateianbindung |
| Browser → Frontend | Next.js SSR/CSR | HTTP |
| CI/CD Pipeline | GitHub Actions → Docker Compose | HTTP (Smoke Test) |

**Mapping fachlich → technisch:**

- Frontend-Container (Port 8000): Next.js/React-Anwendung, dient als Benutzeroberfläche
- Backend-Container (Port 3000): FastAPI-Anwendung, verarbeitet Geschäftslogik und Datenzugriff
- SQLite-Datenbankdatei: Persistiert in einem Docker-Volume (`data`)

---

# Lösungsstrategie

**Inhalt**

Technologieentscheidungen:
- Frontend: HTML, CSS, TypeScript/React (Next.js 16)
- Backend: Python (FastAPI mit Gunicorn/Uvicorn)
- DB: SQLite
- Tests: Pytest (Backend), unittest
- CI/CD: GitHub Actions
- Containerization: Docker / Docker Compose
- IDE: IntelliJ
- Projekt Management: GitHub Projects

**Zentrale Entwurfsentscheidungen:**

| Entscheidung | Begründung |
|--------------|------------|
| Schichtbasierter Architekturstil (ADR04) | Einfache Umsetzung, klare Trennung der Verantwortlichkeiten zwischen Frontend, Backend und Datenbank |
| PBKDF2-HMAC mit SHA256 für Passwort-Hashing (ADR01) | Hohe Sicherheit gegen Brute-Force-Angriffe, Unterstützung durch Python hashlib |
| Direkte Weiterleitung nach Registrierung (ADR02) | Erhöht Benutzerfreundlichkeit, vermeidet unnötige Schritte |
| 3x4 Matrix für Rezeptanzeige (ADR03) | Verhindert Informationsüberladung, Rezeptkacheln sind groß genug für Bilder und Infos |
| Liskov Substitution Principle (ADR05) | Ermöglicht späteren Austausch der Datenquelle ohne Änderung der Geschäftslogik |

Unsere Architekturentscheidungen sind [hier](https://github.com/GalacticCodeGambit/LazyCook/tree/4710a641f177a29e59067edf688781efb3b03a3d/docs/adr) zu finden.

---

# Bausteinsicht

## Whitebox Gesamtsystem

Das Gesamtsystem besteht aus drei Hauptbausteinen: dem Frontend, dem Backend und der Datenbank. Diese sind durch den schichtbasierten Architekturstil klar voneinander getrennt.

**Übersichtsdiagramm:**

```
┌─────────────────────────────────────────────────────────┐
│                      Browser (Nutzer)                   │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP (Port 8000)
┌────────────────────────▼────────────────────────────────┐
│              Frontend (Next.js/React)                   │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ Homepage │  │ Login/       │  │ RecipeFinder      │  │
│  │          │  │ Registrier.  │  │ (Zutateneingabe)  │  │
│  └──────────┘  └──────────────┘  └───────────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │ REST API (JSON, Port 3000)
┌────────────────────────▼────────────────────────────────┐
│              Backend (FastAPI/Python)                   │
│  ┌──────────────────┐  ┌────────────────────────────┐   │
│  │ routes/          │  │ services/                  │   │
│  │ AuthRoutes.py    │  │ AuthService.py             │   │
│  │ RecipeRoutes.py  │  │ UserService.py             │   │
│  │ UserRoutes.py    │  │ RecipeSUCUK.py             │   │
│  └──────────┬───────┘  │ EmailService.py            │   │
│             │           └────────────────────────────┘   │
│  ┌──────────▼───────┐  ┌────────────────────────────┐   │
│  │ core/            │  │ dao/                       │   │
│  │ Database.py      │  │ AccountDAO.py              │   │
│  │ Auth.py          │  │ IngredientDAO.py           │   │
│  │ Models.py        │  │ RecipeDAO.py               │   │
│  └──────────┬───────┘  └────────────────────────────┘   │
└─────────────┼───────────────────────────────────────────┘
              │ SQLite3
┌─────────────▼───────────────────────────────────────────┐
│           SQLite-Datenbank (LazyCookDB.sqlite3)         │
│  Tabellen: Account, User, Recipe, Ingredient,           |
|  IngredientUsage, Exists_from, Author, RefreshToken,    |
|  PasswordResetToken, Favorites                          │
└─────────────────────────────────────────────────────────┘
```

**Begründung:**
Die Zerlegung folgt dem schichtbasierten Architekturstil (ADR04). Das Frontend ist für die Darstellung zuständig, das Backend für die Geschäftslogik und den Datenzugriff, die Datenbank für die Persistenz. Diese klare Trennung ermöglicht unabhängige Entwicklung und einfache Wartbarkeit.

**Enthaltene Bausteine:**

| Name | Verantwortung |
|------|---------------|
| Frontend (Next.js/React) | Benutzeroberfläche, Zutateneingabe, Rezeptanzeige, Login/Registrierung |
| Backend (FastAPI/Python) | REST-API-Endpunkte, Authentifizierung, Rezeptfilterung, Geschäftslogik |
| Datenbank (SQLite) | Persistente Speicherung von Nutzerkonten, Rezepten und Zutaten |

**Wichtige Schnittstellen:**

| Schnittstelle | Beschreibung |
|---------------|--------------|
| POST /auth/login | Anmeldung mit E-Mail und Passwort. Gibt Erfolgsmeldung oder Fehlermeldung zurück |
| POST /auth/register | Registrierung mit E-Mail und Passwort. Passwort wird mit PBKDF2-HMAC gehasht |
| POST /auth/logout | Abmeldung |
| POST /users/me | Profil anzeigen, updaten und löschen |

### Frontend (Next.js/React)

**Zweck/Verantwortung:** Das Frontend ist die Präsentationsschicht der Anwendung. Es stellt die Benutzeroberfläche bereit und kommuniziert über REST-Aufrufe mit dem Backend.

**Schnittstellen:** Kommuniziert über HTTP/JSON mit dem Backend auf Port 3000. Wird im Docker-Container auf Port 8000 ausgeliefert.

**Technologie:** Next.js 16, React 19, TypeScript, Tailwind CSS, Radix UI, Lucide Icons.

**Ablageort:** `project/frontend/`

### Backend (FastAPI/Python)

**Zweck/Verantwortung:** Das Backend bildet die Geschäftslogik-Schicht. Es verarbeitet API-Anfragen, führt Authentifizierung durch, filtert Rezepte und greift auf die Datenbank zu.

**Schnittstellen:** Stellt REST-Endpunkte bereit. Kommuniziert direkt mit der SQLite-Datenbank.

**Technologie:** Python, FastAPI, Gunicorn mit UvicornWorker (4 Worker-Prozesse), Passlib (bcrypt), hashlib (PBKDF2).

**Ablageort:** `project/backend/`

**Paket- und Klassenstruktur:**

`core/` – Querschnittliche Infrastruktur
- `core/Database.py` – SQLite-Verbindung und grundlegende Datenbankfunktionen
- `core/Auth.py` – Token-Logik und Authentifizierungshilfsfunktionen
- `core/Models.py` – Pydantic-Modelle für API-Validierung (z.B. UserSignUpIn, UserResponse, SessionResponse)

`dao/` – Datenzugriffsschicht
- `dao/AccountDAO.py` – CRUD-Operationen für Benutzerkonten
- `dao/IngredientDAO.py` – CRUD-Operationen für Zutaten
- `dao/RecipeDAO.py` – CRUD-Operationen für Rezepte

`domain/` – Domänenmodelle
- `domain/recipe.py` – Domänenklasse Rezept (Name, Zutaten, Zubereitung, Dauer, Bewertung)
- `domain/ingredient.py` – Domänenklasse Zutat (Name, Menge)
- `domain/person.py` – Abstrakte Basisklasse für Nutzer (Name, E-Mail, Passwort, Rolle)

`routes/` – API-Schicht
- `routes/AuthRoutes.py` – FastAPI-Endpunkte für Authentifizierung (Login, Register, Logout)
- `routes/RecipeRoutes.py` – FastAPI-Endpunkte für Rezepte
- `routes/UserRoutes.py` – FastAPI-Endpunkte für Benutzerverwaltung

`services/` – Geschäftslogik
- `services/AuthService.py` – Geschäftslogik für Authentifizierung und Passwortverwaltung
- `services/UserService.py` – Geschäftslogik für Benutzerverwaltung
- `services/RecipeSUCUK.py` – Logik zum Filtern der Rezepte anhand der Zutateneingabe
- `services/EmailService.py` – Versenden automatischer E-Mails (z.B. Passwort vergessen)

Einstiegspunkte
- `LazyCookAdministration.py` – Entry-Point, CORS-Middleware, FastAPI-Start
- `ImportRecipes.py` – Einmaliges Einfügen von Rezepten in die Datenbank

### Datenbank (SQLite)

**Zweck/Verantwortung:** Persistente Speicherung aller Anwendungsdaten.

**Datenbankschema:**

| Tabelle | Spalten | Beschreibung |
|---------|---------|--------------|
| Account | id, email, name, hashedPassword, createdAt | Benutzerkonten mit gehashten Passwörtern |
| RefreshToken | id, AccountID, token, expiresAt, createdAt | Token für die Authentifizierung |
| Recipe | id, name, description, vid | Rezepte |
| Ingredient | id, name, mengenArt | Verfügbare Zutaten |
| Exists_from | zid (FK → Zutat), rid (FK → Rezept), menge | N:M-Beziehung Zutat-Rezept |
| Author | id, name | Rezeptautoren |
| Favorites | AccountID, rid | Favoriten jedes Accounts |

**Ablageort:** `LazyCookDB.sqlite3` (persistiert in Docker-Volume `data`)

## Ebene 2

### Whitebox Frontend

Das Frontend ist als Next.js-Anwendung mit dem App-Router strukturiert:

| Baustein | Verantwortung |
|----------|---------------|
| `app/homepage/` | Startseite mit Hero-Section, Funktionsweise-Erklärung und Login-Modal |
| `app/imports/Startseite.tsx` | Importierte Startseitenkomponenten |
| `app/components/ui/` | Wiederverwendbare UI-Komponenten (Buttons, Calendar, etc.) basierend auf Radix UI/shadcn |

### Whitebox Backend

Das Backend folgt einer paketbasierten Schichtenstruktur:

| Paket / Datei | Verantwortung |
|---------------|---------------|
| `LazyCookAdministration.py` | Entry-Point, CORS-Middleware, FastAPI-Start |
| `core/Database.py` | SQLite-Verbindung und grundlegende Datenbankfunktionen |
| `core/Auth.py` | Token-Logik und Authentifizierungshilfsfunktionen |
| `core/Models.py` | Pydantic-Schemas für Request/Response-Validierung |
| `dao/AccountDAO.py` | CRUD-Operationen für Benutzerkonten |
| `dao/IngredientDAO.py` | CRUD-Operationen für Zutaten |
| `dao/RecipeDAO.py` | CRUD-Operationen für Rezepte |
| `domain/recipe.py`, `domain/ingredient.py`, `domain/person.py` | Domänenmodelle: Rezept-, Zutaten- und Nutzer-Entitäten |
| `routes/AuthRoutes.py` | API-Endpunkte für Authentifizierung (Login, Register, Logout) |
| `routes/RecipeRoutes.py` | API-Endpunkte für Rezepte |
| `routes/UserRoutes.py` | API-Endpunkte für Benutzerverwaltung |
| `services/AuthService.py` | Geschäftslogik für Authentifizierung und Passwortverwaltung |
| `services/UserService.py` | Geschäftslogik für Benutzerverwaltung |
| `services/RecipeSUCUK.py` | Geschäftslogik: Filtern der Rezepte anhand der Zutateneingabe |
| `services/EmailService.py` | Versenden automatischer E-Mails |
| `ImportRecipes.py` | Einmaliges Einfügen von Rezepten in die Datenbank |

---

# Laufzeitsicht

## Szenario 1: Benutzerregistrierung

1. Nutzer gibt E-Mail und Passwort auf der Registrierungsseite ein
2. Frontend sendet POST-Request an `/auth/register` mit E-Mail und Passwort als JSON
3. Backend (`routes/AuthRoutes.py` → `services/AuthService.py`) erzeugt ein 16-Byte zufälliges Salt
4. Backend hasht das Passwort mit PBKDF2-HMAC (SHA256, 100.000 Iterationen)
5. Backend speichert E-Mail, gehashtes Passwort und Salt (jeweils Base64-kodiert) in der Konto-Tabelle via `dao/AccountDAO.py`
6. Backend prüft ob E-Mail bereits existiert und gibt entsprechende Meldung zurück
7. Frontend zeigt Erfolgsmeldung und leitet direkt zum RecipeFinder weiter (ADR02)


## Szenario 2: Benutzeranmeldung

1. Nutzer gibt E-Mail und Passwort auf der Anmeldeseite ein
2. Frontend sendet POST-Request an `/auth/login`
3. Backend (`routes/AuthRoutes.py` → `services/AuthService.py`) ruft `dao/AccountDAO.py` auf, um Salt und gehashtes Passwort aus der Datenbank zu laden
4. Backend hasht das eingegebene Passwort mit dem gespeicherten Salt und vergleicht das Ergebnis
5. Bei Übereinstimmung: Erfolgsmeldung; bei Fehler: Fehlermeldung ("Falsches Passwort" oder "Kein Konto hinterlegt")

## Szenario 3: Rezeptfilterung nach Zutaten

1. Nutzer gibt auf der RecipeFinder-Seite Zutaten (Name, Menge, Einheit) und Personenanzahl ein
2. Zutaten werden im Browser-Cache zwischengespeichert
3. Frontend sendet die Zutatenliste und Personenanzahl als JSON an das Backend
4. Backend filtert die Rezepte in der Datenbank anhand der eingegebenen Zutaten über die Besteht_Aus-Tabelle
5. Backend gibt passende Rezepte als JSON zurück
6. Frontend zeigt maximal 12 Rezepte als 3x4 Matrix auf einer Seite an. Weitere können über einen Button geladen werden (maximal 96 Rezepte) (ADR03)

![UML-Sequenzdiagramm_Rezepte-filtern.drawio.png](https://github.com/GalacticCodeGambit/LazyCook/blob/49d82de42d345200ba9f4e0ddb18b2245cba3c40/docs/UML/UML-Sequenzdiagramm_Rezepte-filtern.drawio.png)

## Szenario 4: Benutzerabmeldung

1. Nutzer klickt auf "Abmelden"
2. Frontend löscht die Sitzungsdaten
3. Nutzer wird zur Startseite weitergeleitet

## Szenario 5: Konto löschen

1. Nutzer klickt auf "Konto löschen"
2. Nutzer erhält einen Bestätigungsdialog
3. Nutzer klickt auf "Bestätigen"
4. Konto ist gelöscht (keine Daten mehr in der Datenbank), Nutzer wird ausgeloggt

## Szenario 6: Email ändern

1. Nutzer klickt auf "Email ändern"
2. Nutzer gibt neue Email ein
3. Neue Email wird hinterlegt
4. Bei neuer Anmeldung muss neue Email eingegeben werden. Die alte ist nicht mehr möglich.

## Szenario 6: Passwort ändern

1. Nutzer klickt auf "Passwort ändern"
2. Nutzer gibt altes Passwort und neues Passwort (zweimal) ein
3. Nuter erhält eine Bestätigunsemail an die hinterlegte Email
4. Bei neuer Anmeldung muss das neue Passwort eingegeben werden

## Szenario 7: Passwort vergessen

1. Nutzer klickt auf "Passwort vergessen"
2. Nutzer gibt seine Email ein
3. Es wird geprüft ob für die Email ein Account hinterlegt ist
4. Nutzer erhält Email mit Link zur Passwortänderungsseite
5. Nutzer gibt neues Passwort ein

## Szenario 8: Rezept suchen nach Titel

1. Nutzer gibt Rezeptnamen in Suchfeld ein
2. Rezepte mit ähnlichem Titel werden in der Datenbank gesucht
3. Rezepte werden im Frontend angezeigt

![UML-Sequenzdiagramm_automatischer-Rezeptvorschlag.png](https://github.com/GalacticCodeGambit/LazyCook/blob/49d82de42d345200ba9f4e0ddb18b2245cba3c40/docs/UML/UML-Sequenzdiagramm_automatischer-Rezeptvorschlag.png)

---

# Verteilungssicht

## Infrastruktur Ebene 1

Die Anwendung wird mittels Docker Compose auf einem einzelnen Host deployed. Zwei Container kommunizieren über ein internes Docker-Netzwerk.

```
┌──────────────────────────────────────────────────────────┐
│                    Host-System                           │
│                                                          │
│  ┌─────────────────────┐    ┌─────────────────────────┐  │
│  │  frontend-dev       │    │  backend                │  │
│  │  (Docker Container) │    │  (Docker Container)     │  │
│  │                     │    │                         │  │
│  │  Base: node:24-     │    │  Base: python:3.11-slim │  │
│  │        alpine3.20   │    │                         │  │
│  │  Port: 8000         │    │  Port: 3000             │  │
│  │                     │    │  Workers: 4 (Gunicorn/  │  │
│  │  Next.js SSR        │    │           Uvicorn)      │  │
│  │                     │    │                         │  │
│  └─────────────────────┘    │  ┌───────────────────┐  │  │
│                             │  │ Volume: /data     │  │  │
│                             │  │ LazyCookDB.sqlite3│  │  │
│                             │  └───────────────────┘  │  │
│                             └─────────────────────────┘  │
│                                                          │
│  Port-Mapping:                                           │
│    localhost:8000 → frontend:8000                        │
│    localhost:3000 → backend:3000                         │
└──────────────────────────────────────────────────────────┘
```

**Begründung:** Docker Compose ermöglicht eine einfache, reproduzierbare Entwicklungs- und Deployment-Umgebung. Die Trennung in zwei Container spiegelt die Schichtarchitektur wider.

**Zuordnung von Bausteinen zu Infrastruktur:**

| Baustein | Container | Dockerfile | Technologie |
|----------|-----------|------------|-------------|
| Frontend | frontend-dev | Dockerfile-frontend | Node.js 24, Next.js 16, React 19 |
| Backend + DB | backend | Dockerfile-backend | Python 3.11, FastAPI, Gunicorn, SQLite |

**CI/CD-Pipeline (GitHub Actions):**
Die CI-Pipeline baut die Docker-Container, startet die Services, wartet auf die Verfügbarkeit des Frontends (Port 8000), führt Backend-Unittests aus und prüft per Smoke-Test die Erreichbarkeit.

---

# Querschnittliche Konzepte

## Sicherheit / Authentifizierung

Passwörter werden niemals im Klartext gespeichert. Stattdessen wird PBKDF2-HMAC mit SHA256 verwendet (ADR01). Pro Nutzer wird ein zufälliges 16-Byte Salt generiert. Der Hash wird mit 100.000 Iterationen berechnet. Salt und Hash werden Base64-kodiert in der Konto-Tabelle gespeichert. Bei der Anmeldung wird das eingegebene Passwort mit dem gespeicherten Salt erneut gehasht und mit dem gespeicherten Hash verglichen.

## CORS (Cross-Origin Resource Sharing)

Das Backend konfiguriert CORS-Middleware, um Anfragen vom Frontend (localhost:8000) an das Backend (localhost:3000) zu erlauben. Alle HTTP-Methoden und Header sind zugelassen.

## Validierung

Die Eingabevalidierung erfolgt auf zwei Ebenen: Im Frontend wird die Benutzereingabe vorab geprüft (z.B. E-Mail-Format), im Backend wird die Validierung durch Pydantic-Modelle (`UserSignUpIn` mit `EmailStr`) sichergestellt. Die Datenbank erzwingt zusätzlich Integritätsbedingungen (UNIQUE, NOT NULL, Foreign Keys).

## Persistenz

SQLite wird als eingebettete Datenbank verwendet. Die Datenbankdatei wird in einem Docker-Volume persistiert, sodass Daten Container-Neustarts überleben. Foreign Keys sind aktiviert (`PRAGMA foreign_keys = ON`). Für jeden Request wird eine neue Datenbankverbindung erstellt (`get_connection()`), um Thread-Safety zu gewährleisten.

## Containerisierung

Die Anwendung wird mit Docker Compose verwaltet. Das Frontend wird als Node.js-Container gebaut (`npm run build` → `npm start`), das Backend als Python-Container mit Gunicorn und 4 Uvicorn-Workern. Ein Docker-Volume (`data`) persistiert die SQLite-Datenbank.

## Fehlerbehandlung

API-Endpunkte verwenden Try-Catch-Blöcke und geben strukturierte JSON-Antworten mit `message`-Feld zurück. Datenbankoperationen verwenden Transaktionen mit Rollback bei Fehlern. Verbindungen werden im `finally`-Block geschlossen.

---

# Architekturentscheidungen

Die wichtigsten Architekturentscheidungen sind als ADRs (Architecture Decision Records) dokumentiert:

| ADR | Titel | Entscheidung |
|-----|-------|--------------|
| ADR01 | Sichere Passwortspeicherung | PBKDF2-HMAC mit SHA256, 100.000 Iterationen, zufälliges Salt, Base64-Kodierung |
| ADR02 | Intuitive Nutzbarkeit | Direkte Weiterleitung von Registrierung zum RecipeFinder (ohne erneute Anmeldung) |
| ADR03 | Verhinderung von Informationsüberladung | 3x3-Matrix für Rezeptanzeige, keine maximale Begrenzung |
| ADR04 | Architekturstil | Schichtbasierter Architekturstil (Frontend → Backend → Datenbank) |
| ADR05 | Designprinzipien | Single Responsibility Principle (SRP) für klare Trennung der Verantwortlichkeiten und Funktionalität |

Alle ADRs sind [hier](https://github.com/GalacticCodeGambit/LazyCook/tree/4710a641f177a29e59067edf688781efb3b03a3d/docs/adr) zu finden.

---

# Qualitätsanforderungen

## Übersicht der Qualitätsanforderungen

| Qualitätsattribut | Verfeinerung | Qualitätsszenario | Geschäftl. Nutzen | Techn. Risiko |
|-------------------|-------------|-------------------|-------------------|---------------|
| Wartbarkeit | Änderbarkeit | Entwickler möchte neues Feature hinzufügen – Änderungen innerhalb von 2 Arbeitstagen | Hoch | Hoch |
| Effizienz | Zeitverhalten | Benutzer filtert Rezepte – Anzeige innerhalb von max. 5 Sekunden | Hoch | Hoch |
| Sicherheit | Sicherheit der Nutzerdaten | Passwort wird gehasht mit Salt in der Datenbank gespeichert | Hoch | Hoch |
| Benutzbarkeit | Bedienbarkeit & Ansehnlichkeit | Registrierung bis RecipeFinder mit möglichst wenigen Klicks; 3x3 Matrix Rezeptanzeige | Mittel | Gering–Mittel |
| Kompatibilität | Interoperabilität | Anwendung läuft auf Chrome, Firefox, Safari, Edge (neueste Version, Laptop) | Hoch | Mittel |

## Qualitätsszenarien

| ID | Q-Attribut | Quelle | Stimulus | Artefakt | Umgebung | Antwort | Antwortmaß |
|----|-----------|--------|----------|----------|----------|---------|------------|
| 01 | Sicherheit | Benutzer | Passwort generieren | Datenbank | Normalbetrieb | Konto korrekt erstellt | Passwort gehasht in der Datenbank vorhanden |
| 02 | Benutzbarkeit | Benutzer | Suchen nach neuem Rezept | System | Normalbetrieb | Benutzer benutzt die Website produktiv | Durchklicken innerhalb von 2 min |
| 03 | Änderbarkeit | Entwickler | Website ändern / neues Feature | Code | Entwicklung | Änderung vorgenommen und getestet | 14 Stunden (2 Arbeitstage) |
| 04 | Kompatibilität | Benutzer | Ruft LazyCook Seite auf | System/Frontend | Normalbetrieb | Seite wird angezeigt | Funktioniert auf Edge, Firefox, Chrome, Opera GX (neueste Version) |
| 05 | Geschwindigkeit | Benutzer | Rezept wird gesucht | System | Normalbetrieb | Rezepte werden angezeigt | Innerhalb von max. 5 Sekunden |

---

# Risiken und technische Schulden

| Risiko/Schuld | Beschreibung | Priorität | Maßnahme |
|---------------|-------------|-----------|----------|
| SQLite-Skalierbarkeit | SQLite unterstützt keine parallelen Schreibzugriffe; bei hoher Nutzerzahl kann es zu Engpässen kommen | Gering | Mittelfristig Migration auf PostgreSQL oder MySQL möglich dank SRP (ADR05) |
| Fehlende maximale Rezeptbegrenzung | Bei vielen Rezepten in der Datenbank gibt es keine Begrenzung der Ergebnisanzahl, was zu langen Ladezeiten führen kann (ADR03) | Mittel | Pagination implementieren |
| Rechtliche Probleme durch Urheberrecht bei Rezepten | Rezepte sind urheberrechtlich geschützt. Rezepte einfach ohen Erlaubnis bereitszustellen könnte zu Rechtlichen Problemen führen | Mittel |  Vorhandene AGBs und Meldebutton, Verlinkung auf Original Rezept in Rezeptansichts zu sehen |
| TODO-Kommentare im Code | Mehrere offene TODOs: Datenbank-Speicherort, E-Mail-Validierung, Passwortstärke, Error Messages generalisieren | Mittel | Systematisch abarbeiten |
| Fehlende Backend-Tests & Frontend-Tests| Einige Backend-Dateien sind nicht mit Tests abgedeckt, Frontend-Tests fehlen vollständig | Hoch | Unittests erweitern, Frontend-Tests hinzufügen |

---

# Glossar

| Begriff | Definition |
|---------|-----------|
| RecipeFinder | Die Hauptseite der Anwendung, auf der Nutzer Zutaten eingeben und passende Rezepte angezeigt bekommen |
| PBKDF2-HMAC | Password-Based Key Derivation Function 2 mit Hash-based Message Authentication Code; sicheres Passwort-Hashing-Verfahren |
| Salt | Zufällig generierter Wert, der vor dem Hashing an das Passwort angehängt wird, um Rainbow-Table-Angriffe zu verhindern |
| ADR | Architecture Decision Record; dokumentierte Architekturentscheidung mit Kontext, Alternativen und Konsequenzen |
| SRS | Software Requirements Specification; Softwareanforderungsspezifikation |
| REST | Representational State Transfer; Architekturstil für Web-APIs |
| CORS | Cross-Origin Resource Sharing; Mechanismus zum Erlauben von Cross-Origin-Anfragen im Browser |
| SRP | Single Responsibility Principle; Designprinzip, das sicherstellt, dass Verantwortlichkeiten in Klassen getrennt werden |
| Docker Compose | Tool zur Definition und Verwaltung von Multi-Container-Docker-Anwendungen |
| FastAPI | Modernes Python-Web-Framework für den Aufbau von APIs |
| Next.js | React-Framework für serverseitiges Rendering und statische Seitengenerierung |
| SQLite | Eingebettete relationale Datenbank ohne separaten Serverprozess |
| CI/CD | Continuous Integration / Continuous Deployment; automatisierte Build- und Deployment-Pipeline |
| Gunicorn | Python WSGI HTTP Server, hier mit Uvicorn-Workern für ASGI-Support |
