# Testbericht
(Stand: 2026-06-03)

## Einleitung
Dieser Testbericht dokumentiert den aktuellen Testumfang der Anwendung **LazyCook**. Der Schwerpunkt lag auf dem Backend, da dort zentrale fachliche Funktionen wie Authentifizierung, Datenbankzugriffe, Passwortprüfung, Token-Verarbeitung, E-Mail-Validierung und die Rezeptsuche umgesetzt sind. Zusätzlich wird der Build- und Smoke-Test-Prozess aus der CI-Pipeline berücksichtigt.

Ziel der Testaktivitäten war es, die fachlichen Kernfunktionen gegen typische Fehlerfälle abzusichern und sicherzustellen, dass sich die Anwendung in der Container-Umgebung zuverlässig bauen und starten lässt.
<br>Dafür wurde eine Testabdeckung von 30% des Backend-Codes angestrebt, wobei die wichtigsten Funktionalitäten priorisiert wurden. 

## Teststrategie
Für LazyCook wird eine risikoorientierte Teststrategie verwendet. Kritische Kernbereiche wie Login, Registrierung, Token-Verarbeitung, Passwortvalidierung und Datenbankoperationen werden mit automatisierten Tests abgesichert. Dabei kommen folgende Testarten zum Einsatz:

- **Unit-Tests** für isolierte Funktionen, z.B. Passwort- und E-Mail-Validierung sowie Token-Erzeugung und -Prüfung.
- **Integrationsnahe Tests** für Datenbankfunktionen, bei denen eine isolierte Testdatenbank verwendet wird.
- **Mock-basierte Tests** für Abhängigkeiten wie Datenbankzugriffe oder tokenbezogene Hilfsfunktionen.
- **Smoke-Tests** in der CI-Pipeline, um die Weboberfläche nach dem Start kurz zu prüfen.
- **Build- und Konfigurationsprüfungen** über Docker Compose und GitHub Actions (CI-Pipeline).

Verwendete Werkzeuge und Frameworks:

- **Pytest** als Test-Framework
- **unittest.mock** für Mocks und Patchings
- **Docker / Docker Compose** für reproduzierbare Testumgebungen
- **GitHub Actions** für die automatisierte CI-Ausführung
- **GitHub Super-Linter** für zusätzliche Qualitätsprüfungen von Code- und Konfigurationsdateien

## Testplan
Die Testaktivitäten wurden in folgende Schritte gegliedert:

1. Aufbau der Container-Umgebung mit `docker compose -f project/compose.yaml build`
2. Start der Dienste mit `docker compose -f project/compose.yaml up -d`
3. Prüfung, ob das Frontend unter `http://localhost:8000` erreichbar ist
4. Ausführung der Backend-Tests mit `pytest`
5. Prüfung von Sonderfällen wie ungültige E-Mail-Adressen, schwache Passwörter, abgelaufene Tokens und leere Datenmengen
6. Analyse der Ergebnisse und Ableitung von Verbesserungen

Ressourcen:

- Entwicklungsumgebung mit Python und Docker
- Isolierte Testdatenbank pro Testlauf
- Automatisierte CI-Pipeline auf GitHub Actions

Zeitlich wurden die Tests als wiederholbarer Bestandteil der Entwicklung eingeplant, insbesondere vor dem Merge in `main` und `blatt*` bzw. vor Pull-Requests.

## Testfälle
Im Repository sind aktuell **74 automatisierte Backend-Testfälle** in sechs Testmodulen vorhanden. Die Testfälle decken die wichtigsten Funktionsbereiche ab:

| Bereich | Testumfang | Status |
|---|---|---|
| E-Mail-Validierung | Gültige und ungültige E-Mail-Formate | bestanden |
| Passwortvalidierung | Mindestlänge, Groß-/Kleinbuchstaben, Zahlen, Sonderzeichen | bestanden |
| Passwort-Hashing | Hash-Erzeugung und Verifikation | bestanden |
| JWT-/Token-Logik | Access Tokens, Refresh Tokens, Reset Tokens, Ablaufprüfung | bestanden |
| Datenbankzugriffe | Account anlegen, lesen, ändern, löschen | bestanden |
| Datenbank-Token | Refresh-Tokens und Passwort-Reset-Tokens speichern, lesen, löschen | bestanden |
| Rezept- und Zutatenverwaltung | Rezepte anlegen, Zutaten anlegen, Verknüpfung, Auslesen | bestanden |
| Zutaten-Nutzung | Zählung und Normalisierung der häufig verwendeten Zutaten | bestanden |
| Rezeptvorschlag-Logik | Trefferbewertung, Sortierung, Paginierung | bestanden |
| CI-Smoketest | Erreichbarkeit des Frontends nach dem Start | bestanden |

Beispiele für dokumentierte Testfälle:

- Registrierung mit gültiger E-Mail und sicherem Passwort
- Ablehnung ungültiger E-Mail-Adressen
- Ablehnung zu schwacher Passwörter
- Erzeugung und Validierung von Access- und Refresh-Tokens
- Behandlung abgelaufener oder bereits verwendeter Reset-Tokens
- Anlegen und Abrufen von Konten in einer isolierten Testdatenbank
- Verknüpfen von Zutaten mit Rezepten und Prüfen der Rezeptbewertung

## Testergebnisse
Die vorhandene Testsuite deckt die zentralen Fachfunktionen von LazyCook gut ab. Die Ergebnisse zeigen, dass:

- die Passwort- und E-Mail-Validierung korrekt arbeitet,
- JWT-basierte Tokens erzeugt und geprüft werden können,
- Datenbankoperationen für Konten, Tokens, Rezepte und Zutaten konsistent funktionieren,
- die Rezeptsuche auf Basis von Zutaten korrekt bewertet und sortiert wird,
- die CI-Pipeline den Build sowie einen Frontend-Smoke-Test ausführt.

Im dokumentierten Testumfang sind **keine offenen kritischen Fehler** bekannt. Risiken bleiben vor allem dort, wo bislang nur Unit- und Mock-Tests eingesetzt werden, aber noch keine vollständigen End-to-End-Tests oder Lasttests vorhanden sind.

## Metriken
Quantitative Kennzahlen des aktuellen Teststands:

- **Anzahl automatisierter Testfälle:** 74
- **Anzahl Testmodule:** 6 Backend-Testmodule
- **CI-Smoke-Tests für das Frontend:** 1
- **Bekannte Fehler im betrachteten Testumfang:** 0
- **Automatisierte Code-Coverage-Messung:** derzeit im Workflow dokumentiert als "SonarCloud Full Metrics (main branch)"
- **Mittlere Fehlerbehebungszeit:** nicht gemessen

Weitere sinnvolle Metriken für zukünftige Testläufe wären Code-Coverage in Prozent, Laufzeit pro Testmodul und die Anzahl fehlschlagender CI-Läufe pro Sprint (siehe GitHub Actions).

## Empfehlungen
Für eine weitere Verbesserung der Testqualität werden folgende Maßnahmen empfohlen:

1. **End-to-End-Tests ergänzen**, um Login, Registrierung und Rezeptsuche im Zusammenspiel von Frontend und Backend zu prüfen.
2. **Negative Testfälle erweitern**, z.B. fehlerhafte Eingaben, Datenbankkonflikte und Netzwerkfehler.
3. **Regressionstests regelmäßig in CI ausführen**, damit Änderungen an Authentifizierung oder Datenbanklogik sofort auffallen.
4. **Last- und Stabilitätstests** für zentrale Benutzeraktionen ergänzen, sobald die Anwendung produktiver genutzt wird.

## Schlussfolgerung
Die aktuelle Testbasis von LazyCook ist solide und konzentriert sich auf die sicherheits- und fachlich relevanten Kernbereiche. Mit 74 automatisierten Testfällen, isolierten Datenbanktests und einer CI-Pipeline mit Build- und Smoke-Test besteht eine gute Grundlage für zuverlässige Weiterentwicklung.

Für den produktiven Einsatz sollten als nächster Schritt vor allem End-to-End-Tests und erweiterte Integrationsprüfungen ergänzt werden. Insgesamt ist die Softwarequalität im getesteten Umfang als **gut** einzustufen.
