# LazyCook
## Softwareanforderungen
___
### 1. Einleitung

#### 1.1 Übersicht

Schlichtes/modernes Design, einfache Bedienbarkeit, gute Übersicht, viele Rezepte, einfacher Start

#### 1.2 Geltungsbereich

In diesem Dokument wird das gesamte System von LazyCook behandelt. Es deckt sowohl funktionale als auch nicht-funktionale Anforderungen ab.

#### 1.3 Definitionen, Akronyme und Abkürzungen

| Abkürzung | Erklärung                          |
|-----------|------------------------------------|
| UI        | user interface                     |
| IDE       | integrated development environment |
| n/a       | not applicable                     |

#### 1.4 Referenzen

| Titel                                                               | Datum      | Veröffentlicht bei |
|---------------------------------------------------------------------|------------|--------------------|
| [GitHub - LazyCook](https://github.com/GalacticCodeGambit/LazyCook) | 22.10.2025 | LazyCook Team      |

___
### 2. Funktionale Anforderungen

#### 2.1 Übersicht

LazyCook soll eine Webanwendung sein. Sie soll es ermöglichen, seine vorhandenen Zutaten einzutragen, und daraufhin mögliche Rezepte/Gerichte-vorschlagen, die sich aus diesen Zutaten zubereiten lassen.

#### 2.2 Zutaten hinzufügen können
##### User Story: https://github.com/GalacticCodeGambit/LazyCook/issues/23

##### UI-Mockup:
![](docs/mockup/Zutateneingabe.png)
![](docs/mockup/Zutaten_eingabe_Tomate.png)

##### UML:
<!-- %% Der Nutzer soll beim Eintragen passende Zutaten vorgeschlagen bekommen, die er auswählen kann. -->
>`+ Text`
`+ Bild`

##### Voraussetzungen:
Der Nutzer muss angemeldet sein und sich auf der Seite befinden für Zutaten eintragen, um die Zutaten eintragen zu können.

##### Nachbedingungen:
Die eingetragene Zutat werden gespeichert.

##### Geschätzter Aufwand: mittel/hoch


#### 2.3 Zutaten entfernen können
##### User Story: https://github.com/GalacticCodeGambit/LazyCook/issues/24

##### UI-Mockup:
![](docs/mockup/Zutaten_eingabe_Tomate.png)
![](docs/mockup/Zutateneingabe.png)

##### UML:
>`+ Text`
<img width="1404" height="669" alt="image" src="https://github.com/user-attachments/assets/0717ae89-5dc7-4e61-ba25-2e1cb2c69c54" />


##### Voraussetzungen:
Der Nutzer muss angemeldet sein und sich auf der Seite befinden für Zutaten eintragen, um die Zutaten eintragen zu können und es muss mindestens eine Zutat bereits eingetragen sein.
##### Nachbedingungen:
Die gelöschte Zutat wird aus dem Speicher gelöscht.
##### Geschätzter Aufwand: niedrig


#### 2.4 Automatischer Rezepte vorgeschlagen auf Grundlage der eingetragenen Zutaten
##### User Story: https://github.com/GalacticCodeGambit/LazyCook/issues/25

##### UI-Mockup:
>`+ Bild`

##### UML:
>`+ Text`
<img width="1404" height="669" alt="image" src="https://github.com/user-attachments/assets/0fa4f1cc-b792-4dc3-829e-5bc9e7dd2011" />


##### Voraussetzungen:
Der Nutzer muss angemeldet sein und Zutaten, die er vorrätig hat, eingetragen haben.
##### Nachbedingungen:
n/a
##### Geschätzter Aufwand: hoch


#### 2.5 Als Kunde mit neuem Konto registrieren können
##### User Story: https://github.com/GalacticCodeGambit/LazyCook/issues/26

##### UI-Mockup:
![](docs/mockup/Registrieren.png)

##### UML:
>`+ Text`
<img width="1151" height="599" alt="image" src="https://github.com/user-attachments/assets/e9d58164-48cf-4007-a4bd-af42841ef019" />


##### Voraussetzungen:
Ein Nutzer der LazyCook nutzen will
##### Nachbedingungen:
n/a
##### Geschätzter Aufwand: mittel


#### 2.6 Als Kunde mit Konto anmelden können
##### User Story: https://github.com/GalacticCodeGambit/LazyCook/issues/27

##### UI-Mockup:
![](docs/mockup/Anmelde_Screen.png)

##### UML:
>`+ Text`
<img width="1029" height="491" alt="image" src="https://github.com/user-attachments/assets/31a4661b-3b8f-441f-ba3d-121a4c254923" />


##### Voraussetzungen:
Der User muss mit dem Konto bereits registriert sein mit welchen er sich anmelden möchte.
##### Nachbedingungen:
Der User ist mit dem Konto angemeldet, welches er eingegeben hat.
##### Geschätzter Aufwand: mittel


#### 2.7 Als Kunde mit Konto abmelden können
##### User Story: https://github.com/GalacticCodeGambit/LazyCook/issues/28

##### UI-Mockup:
>![]()

##### UML:
>`+ Text`
`+ Bild`
##### Voraussetzungen:
Der Nutzer muss angemeldet sein mit einem Konto.
##### Nachbedingungen:
Der Nutzer ist nicht angemeldet.
##### Geschätzter Aufwand: niedrig


#### 2.8 Personenanzahl angegeben bei Zutaten eintragen
##### User Story: https://github.com/GalacticCodeGambit/LazyCook/issues/30

##### UI-Mockup:
>`+ Bild`

##### UML:
>`+ Text`
<img width="1404" height="669" alt="image" src="https://github.com/user-attachments/assets/10cea492-6933-4d3d-9839-5889a14f20f2" />


##### Voraussetzungen:
Der Nutzer muss angemeldet sein und sich auf der Seite befinden für Zutaten eintragen, um die Personenanzahl eintragen zu können.
##### Nachbedingungen:
Die eingetragene Personenanzahl wir gespeichert. Bei dem automatischen Rezeptvorschlag wird die Personenanzahl berücksichtigt und passt entsprechend angepasst.
##### Geschätzter Aufwand: mittel


#### 2.9 Grundlegende Zutaten werden beim Eintragen empfohlen 
##### User Story: https://github.com/GalacticCodeGambit/LazyCook/issues/31

##### UI-Mockup:
>`+ Bild`

##### UML:
>`+ Text`
<img width="1404" height="669" alt="image" src="https://github.com/user-attachments/assets/7fd98fa4-d8ca-4d60-ad3c-84e2fb2fd0ae" />


##### Voraussetzungen:
Der Nutzer muss angemeldet sein und sich auf der Seite befinden für Zutaten eintragen.
##### Nachbedingungen:
Die hinzugefügten Grundzutaten müssen zu den bereits vorhandenen Zutaten hinzugefügt werden. 
##### Geschätzter Aufwand: mittel


___
### 3. Nicht-funktionale Anforderungen
Das Projekt muss zum Ende des 4. Semesters abgegeben werden, genaueres wird noch bekannt gegeben. Es muss sich um eine webbasierte Anwendung handeln. LazyCook soll für die Benutzung/Bedingung am Laptop oder am Computer optimiert sein.

#### 3.1 Verwendete Technologien
- Frontend: HTML, CSS, JavaScript/React
- Backend: Python
- DB: SQLite
- IDE: PyCharm
- Projekt Management: GitHub Projects

___
### 4. Unterstützende Informationen
Für weitere Informationen können Sie sich an das LazyCook Team wenden oder unseren ([LazyCook-Discussions](https://github.com/GalacticCodeGambit/LazyCook/discussions)) besuchen. 
