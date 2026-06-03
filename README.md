# LazyCook
[![ci.yml](https://github.com/GalacticCodeGambit/LazyCook/actions/workflows/ci.yml/badge.svg)](https://github.com/GalacticCodeGambit/LazyCook/actions/workflows/ci.yml)
[![lint.yml](https://github.com/GalacticCodeGambit/LazyCook/actions/workflows/lint.yml/badge.svg)](https://github.com/GalacticCodeGambit/LazyCook/actions/workflows/lint.yml)
[![SonarCloud Full Metrics (main branch)](https://github.com/GalacticCodeGambit/LazyCook/actions/workflows/sonarqube-main.yml/badge.svg)](https://github.com/GalacticCodeGambit/LazyCook/actions/workflows/sonarqube-main.yml)

LazyCook soll eine Webanwendung sein, die es ermöglicht, vorhandene Zutaten einzutragen. Darauf basierend soll LazyCook mögliche Rezepte/Gerichte vorschlagen, die du aus diesen Zutaten machen kannst.

## Star History

<a href="https://www.star-history.com/?repos=GalacticCodeGambit%2FLazyCook&type=timeline&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=GalacticCodeGambit/LazyCook&type=timeline&theme=dark&legend=bottom-right" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=GalacticCodeGambit/LazyCook&type=timeline&legend=bottom-right" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=GalacticCodeGambit/LazyCook&type=timeline&legend=bottom-right" />
 </picture>
</a>

## Features
- [x] [#23](https://github.com/GalacticCodeGambit/LazyCook/issues/23) Zutaten hinzufügen können 
- [x] [#24](https://github.com/GalacticCodeGambit/LazyCook/issues/24) Zutaten entfernen können  
- [ ] [#25](https://github.com/GalacticCodeGambit/LazyCook/issues/25) Rezepte/Gerichte automatisch vorgeschlagen bekommen auf Grundlage der eingetragenen Zutaten
- [ ] [#30](https://github.com/GalacticCodeGambit/LazyCook/issues/30) Personenzahl hinzufügen können und vorgeschlagene Rezept/Gericht Größe automatisch anpassen 
- [x] [#27](https://github.com/GalacticCodeGambit/LazyCook/issues/27) Als User mit Konto anmelden können
- [x] [#26](https://github.com/GalacticCodeGambit/LazyCook/issues/26) Als User mit neuem Konto registrieren können

### Optionale Features
- [ ] KI-basierte Rezeptvorschläge Einbindung
- [ ] [#33](https://github.com/GalacticCodeGambit/LazyCook/issues/33) Alle gespeicherten Zutaten aus der Datenbank, sollen auf einer Seite angezeigt werden und Suchbar sein z.B. nach Gerichtname "Pizza".
- [ ] Auf der Zutaten-Seite, werden grundlegende Zutaten wie z.B. Tomaten, Mehl, Salz und Milch automatisch vorgeschlagen. Diese sollen hinzufügbar oder ignorierbar sein.
- [x] [#46](https://github.com/GalacticCodeGambit/LazyCook/issues/46) Konto löschen/bearbeiten können 
- [ ] Fehlende Zutaten werden von einem Rezept in einer Einkaufliste aufgelistet
- [ ] Der Nutzer kann Rezepte in die Datenbank hinzufügen/erstellen 
- [x] [#47](https://github.com/GalacticCodeGambit/LazyCook/issues/47) Der Nutzer kann bereits hinzugefügte Zutaten bearbeiten, wie z.B. Menge, Einheit
- [x] [#45](https://github.com/GalacticCodeGambit/LazyCook/issues/45) Passwörter "sicher" in Datenbank Abspeichern als Hash und vom Frontend/Backend "sicher" behandeln

 ## Installation und Setup
1. Klonen das Repository:  
   `git clone https://github.com/GalacticCodeGambit/LazyCook.git`
2. Navigieren zum Projektverzeichnis:  
   `cd LazyCook/project`
3. Starten der Anwendung mit: Docker Compose:
   `docker compose up --build -d`
<!--Unterschied zu "docker compose up -d"? -->
Die Anwendung sollte jetzt unter `http://localhost:8000` erreichbar sein.

Für die Funktion [#115](https://github.com/GalacticCodeGambit/LazyCook/issues/115) von Email Versenden/Empfangen muss im Ordner `project/` eine `.env` Datei mit den folgenden Variablen angelegt werden:
```
GMAIL_USER=<dein.mail@gmail.com>
GMAIL_PASSWORD=<dein_gmail_passwort>
JWT_SECRET_KEY=<ein_langes_zufallssecret>
```

Hinweis: `JWT_SECRET_KEY` sollte in produktiven Umgebungen immer gesetzt und einzigartig sein. Für lokale Tests nutzt `compose.yaml` einen Dev-Default, damit der erste Start nicht abbricht.

## Verwendete Technologien
- Frontend: HTML, CSS, TypeScript/React
- Backend: Python
- DB: SQLite
- Tests: Pytest
- CI/CD: GitHub Actions
- Containerization: Docker
- Projekt Management: GitHub Projects

### Code-Quality / Linting
- Der Workflow `.github/workflows/lint.yml` prüft das Projekt mit **GitHub Super-Linter**.
- Dabei werden u.a. Python-, TypeScript-, JavaScript-, YAML- und Dockerfile-Dateien validiert.

<!-- 
- Mockup: Figma
- UML: UMLet/Drawio
-->

## Entwicklung
### Linter
#### Python `Black`
Automatisch formatieren:
```
black project/backend/ .
```

`Black` installieren:
```
python -m pip install black
```

### Probleme beim Entwickeln

Problem: Code hinzugefügt/geändert aber Änderungen werden nicht übernommen von Docker 
```
docker compose -f compose.yaml up --build --force-recreate -d  
```

 <!-- ## How It Works -->

 <!-- ## Contributing -->
