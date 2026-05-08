# LazyCook
[![ci.yml](https://github.com/GalacticCodeGambit/LazyCook/actions/workflows/ci.yml/badge.svg)](https://github.com/GalacticCodeGambit/LazyCook/actions/workflows/ci.yml)
[![lint.yml](https://github.com/GalacticCodeGambit/LazyCook/actions/workflows/lint.yml/badge.svg)](https://github.com/GalacticCodeGambit/LazyCook/actions/workflows/lint.yml)

LazyCook soll eine Webanwendung sein. Die es ermöglichen seine vorhanden Zutaten einzutragen und darauf soll LazyCook dir mögliche Rezepte/Gerichte vorschlagen die du aus diesen Zutaten gemacht werden können.   

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

## Verwendete Technologien
- Frontend: HTML, CSS, TypeScript/React
- Backend: Python
- DB: SQLite
- Tests: Pytest
- CI/CD: GitHub Actions
- Containerization: Docker
- Projekt Management: GitHub Projects

## Code-Quality / Linting
- Der Workflow `.github/workflows/ci.yml` prüft mit dem Job `linter` das Projekt mit **GitHub Super-Linter**.
- Dabei werden u. a. Python-, TypeScript-, JavaScript-, YAML- und Dockerfile-Dateien validiert.

<!-- 
- Mockup: Figma
- UML: UMLet/Drawio
-->

 ## Installation and Setup
1. Klonen das Repository:  
   `git clone https://github.com/GalacticCodeGambit/LazyCook.git`
2. Navigieren zum Projektverzeichnis:  
   `cd LazyCook/Project`
3. Starten der Anwendung mit: Docker Compose:
   `docker compose up --build -d`
<!--Unterschied zu "docker compose up -d"? -->
Die Anwendung sollte jetzt unter `http://localhost:8000` erreichbar sein.

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
