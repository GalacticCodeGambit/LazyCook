# LazyCook
## Softwareanforderungen

### 1. Einleitung

#### 1.1 Übersicht

Schlichtes/modernes Design, einfache Bedienbarkeit, gute Übersicht, viele Rezepte, einfacher Start

#### 1.2 Geltungsbereich

In diesem Dokument wird das gesamtes System von LazyCook behandelt. Es deckt sowohl funktionale als auch nicht-funktionale Anforderungen ab.

#### 1.3 Definitionen, Akronyme und Abkürzungen

| Abkürzung | Erklärung                          |
| --------- | ---------------------------------- |
| tbd       | to be determined                   |
| UI        | user interface                     |
| IDE       | integrated development environment |

#### 1.4 Referenzen

| Title                                                               | Date       | Publishing organization |
| ------------------------------------------------------------------- | ---------- | ----------------------- |
| [GitHub - LazyCook](https://github.com/GalacticCodeGambit/LazyCook) | 22.10.2025 | LazyCook Team           |

### 2. Funktionale Anforderungen

#### 2.1 Übersicht

LazyCook soll eine Webanwendung sein. Die es ermöglichen seine vorhanden Zutaten einzutragen und darauf soll LazyCook dir mögliche Rezepte/Gerichte vorschlagen die du aus diesen Zutaten gemacht werden können.

___
Funktionale Anforderungen:
- Zutaten eintragen (Zutaten hinzufügen können):
  Mengenangabe/Personenangabe, Zutateneingabe mit ähnlichen Vorschlägen
- (Personenzahl hinzufügen können und vorgeschlagene Rezept/Gericht Größe automatisch anpassen)
- Zutaten löschen (Zutaten entfernen können)
- Rezept/Gericht Vorschlag anhand der eingetragenen Zutaten bekommen
  (Rezepte/Gerichte automatisch vorgeschlagen bekommen auf Grundlage der eingetragenen Zutaten)
- Anmelden können (Als Kunde mit Konto anmelden können)
- Registrieren können (Als Kunde mit neuem Konto registrieren können)

Nicht funktionale Anforderungen:
- Webbasierte Anwendung
- Abgabe: 4. Semester (genaueres tbd.)
- Programmiersprache/Technologies Used:
    - Frontend: HTML, CSS, (JavaScript) React
    - Backend: Python
    - Datenbank: SQLite
___
#### 2.2 Zutaten hinzufügen können
##### User Story: https://github.com/GalacticCodeGambit/LazyCook/issues/23

##### UI-Mockup:
>`+ Bild`

##### UML:
>`+ Text`
`+ Bild`

##### Voraussetzungen:
Der Nutzer muss angemeldet sein und sich auf der entsprechenden Seite befinden, um die Zutaten eintragen zu können.

##### Nachbedingungen:
Die eingetragene Zutat wir gespeichert.

##### Geschätzter Aufwand: mittel


#### 2.3 Zutaten entfernen können
##### User Story: https://github.com/GalacticCodeGambit/LazyCook/issues/24

##### UI-Mockup:
>`+ Bild`

##### UML:
>`+ Text`
`+ Bild`

##### Voraussetzungen:
Der Nutzer muss angemeldet sein und sich auf der entsprechenden Seite befinden, um die Zutaten eintragen zu können und es muss mindestens eine Zutat bereits eingetragen sein.

##### Nachbedingungen:

##### Geschätzter Aufwand: niedrig


#### 2.4 Automatischer Rezepte vorgeschlagen auf Grundlage der eingetragenen Zutaten
##### User Story: https://github.com/GalacticCodeGambit/LazyCook/issues/25

##### UI-Mockup:
>`+ Bild`

##### UML:
>`+ Text`
`+ Bild`

##### Voraussetzungen:

##### Nachbedingungen:

##### Geschätzter Aufwand: hoch


#### 2.5 Als Kunde mit neuem Konto registrieren können
##### User Story: https://github.com/GalacticCodeGambit/LazyCook/issues/26

##### UI-Mockup:
>`+ Bild`

##### UML:
>`+ Text`
`+ Bild`

##### Voraussetzungen:

##### Nachbedingungen:

##### Geschätzter Aufwand: mittel

#### 2.6 Als Kunde mit Konto anmelden können
##### User Story: https://github.com/GalacticCodeGambit/LazyCook/issues/27

##### UI-Mockup:
>`+ Bild`

##### UML:
>`+ Text`
`+ Bild`

##### Voraussetzungen:
Der User muss mit dem Konto bereits Registriert sein mit welchen er sich anmelden möchte.
##### Nachbedingungen:
Der User ist mit dem Konto angemeldet welches er eingegeben hat.

##### Geschätzter Aufwand: mittel


#### 2.7 Als Kunde mit Konto abmelden können
##### User Story:

##### UI-Mockup:
>`+ Bild`

##### UML:
>`+ Text`
`+ Bild`
##### Voraussetzungen:
Der Nutzer muss angemeldet sein mit einem Konto.
##### Nachbedingungen:
Der Nutzer ist nicht angemeldet.
##### Geschätzter Aufwand: niedrig


### 3. Nicht-funktionale Anforderungen

#### 3.1 Verwendete Technologien
- Frontend: HTML, CSS, JavaScript/React
- Backend: Python
- DB: SQLite
- IDE: PyCharm
- Projekt Management: GitHub Projects

### 4. Technische Einschränkungen

### 5.  Unterstützende Informationen
Für weitere Informationen können Sie sich an das LazyCook Team wenden oder unseren ([LazyCook-Discussions]([GalacticCodeGambit/LazyCook · Discussions · GitHub](https://github.com/GalacticCodeGambit/LazyCook/discussions))) besuchen. 