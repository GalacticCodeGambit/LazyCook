# LazyCook Backend – Single Responsibility Principle (SRP)

## Was ist SRP?

Das Single Responsibility Principle besagt: **Eine Klasse oder ein Modul soll genau einen Grund zur Änderung haben.** Jede Einheit kapselt eine einzige, klar umrissene Verantwortung. Ändert sich eine Anforderung, betrifft das idealerweise nur eine Datei.

## Abgrenzung: SRP vs. LSP

SRP wird gelegentlich mit anderen SOLID-Prinzipien vermischt. Zur Klarstellung: Das **Liskov Substitution Principle (LSP)** betrifft Vererbung — Objekte eines Subtyps müssen überall dort einsetzbar sein, wo der Basistyp erwartet wird, ohne das Verhalten zu brechen. SRP dagegen betrifft die **Aufteilung von Verantwortlichkeiten** und ist unabhängig von Vererbung. Im LazyCook-Backend steht SRP im Fokus, weil es keine nennenswerten Vererbungshierarchien gibt (die Domain-Objekte sind eigenständige Datenklassen) — die zentrale Designfrage war hier „Wer ist wofür zuständig?", nicht „Sind Subtypen austauschbar?".

## Warum SRP für die Entwicklung sinnvoll ist

Ein nach SRP geschnittenes System ist im Alltag spürbar leichter zu entwickeln:

- **Wartbarkeit** — Eine Änderung am Hashing-Algorithmus betrifft nur `core/Auth.py`, eine Schema-Änderung nur den passenden DAO. Man weiß sofort, wo man suchen muss.
- **Isolierte Testbarkeit** — Domain-Objekte ohne DB-Abhängigkeit lassen sich ohne Mocks instanziieren; Geschäftslogik im Service ist direkt unit-testbar, statt versteckt in einer HTTP-Route.
- **Weniger Seiteneffekte** — Klar getrennte Module reduzieren das Risiko, dass eine Änderung an der E-Mail-Logik versehentlich die Token-Verwaltung bricht.
- **Paralleles Arbeiten** — Mehrere Personen können an Routes, Services und DAOs gleichzeitig arbeiten, ohne sich ständig in denselben Dateien zu überschneiden.

## Ausgangslage: SRP-Verletzungen vor dem Refactoring

Vor dem Umbau bündelten mehrere Dateien zu viele Aufgaben:

| Datei | Verantwortlichkeiten (zu viele) |
|---|---|
| `Routes.py` | DB-Zugriff + Passwortvalidierung + E-Mail-Versand in einer Funktion |
| `Auth.py` | 5 Aufgaben: Hashing, JWT, Validierung, Refresh-Token-DB, Password-Reset-DB |
| `Database.py` | SQL für **alle** Entitäten (Account, Rezept, Zutat, Token) — 350 Zeilen |
| `Recipe.py` / `Ingredient.py` | Domain-Objekte griffen über `saveInDB()` direkt auf die Datenbank zu |

Die Folge: jede dieser Dateien hatte mehrere, voneinander unabhängige Gründe zur Änderung — der klassische SRP-Verstoß.

## Was sich im Code-Aufbau geändert hat

Der Code wurde in Module mit je **einer** Verantwortung aufgeteilt:

```
routes/     → nur HTTP-Ein-/Ausgabe (keine Geschäftslogik)
services/   → nur Geschäftsregeln (kein HTTP, kein SQL)
dao/        → nur SQL-Zugriffe
domain/     → nur Datenobjekte (keine externen Abhängigkeiten)
core/       → Querschnitt: Auth-Krypto, DB-Verbindung, Pydantic-Schemas
```

**Konkrete Beispiele:**

*Domain-Objekt ohne DB-Zugriff* — `Recipe` enthält nur noch Attribute und Getter/Setter; das Speichern übernimmt `dao/RecipeDAO.py`. Das Domain-Objekt hat damit keinen DB-bezogenen Änderungsgrund mehr.

*Route delegiert an Service* — `updateCurrentUser` führte früher Validierung, DB-Update und E-Mail-Versand selbst aus. Heute ruft die Route nur noch `user_service.updateUser(...)` auf; die Logik liegt im Service.

*`Auth.py` entschlackt* — von 5 Aufgaben auf 3 reduziert (JWT, Hashing, Validierung + FastAPI-Dependency). Token-Orchestrierung und Reset-Token-Logik wanderten nach `services/AuthService.py`.

*`Database.py` → DAOs* — die zentrale SQL-Sammeldatei wurde aufgeteilt; `Database.py` behält nur noch Verbindungsmanagement und `initDB()`.

*Zwei Dateien → ein Service* — `RecipeSUCUK.py` und `SearchRecipeNames.py` doppelten dieselbe `getAllRecipes()`-Initialisierung; beide wurden in `services/RecipeSUCUK.py` (Recipe-Service) zusammengeführt.

## Ergebnis

| Metrik | Vorher | Nachher |
|---|---|---|
| Gründe zur Änderung pro Datei | mehrere (God-Klassen) | **genau einer** |
| Zeilen in `Database.py` | 350 | **136** |
| Zeilen in `Auth.py` | 130 | **96** |
| Ø Zyklomatische Komplexität | ~3,5 (`Routes.py`-Funktionen) | **1,73** (106 Blöcke, App-Code) |
| Komplexeste Funktion | B(8) `updateCurrentUser` (in Route) | B(9) `updateUser` (isoliert im Service) |
| Testbare Domain-Objekte | ❌ (DB-Abhängigkeiten) | ✅ (ohne externe Abhängigkeiten) |
| Tests | 74 ✅ | 74 ✅ |

Jede Datei hat heute genau einen Grund zur Änderung — SRP ist im Backend durchgängig umgesetzt, ohne dass Funktionalität verloren ging.
