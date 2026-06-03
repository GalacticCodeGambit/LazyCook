# Designprinzipien

## Kontext und Problemstellung

Welcher Designprinzipien soll für das Projekt verwendet werden? Um eine einheitliche Umsetzung im gesamten Projekt zu gewährleisten. 


## Betrachtete Varianten

* Single Responsibility Principle (SRP)
* Open-Closed Principle (OCP)
* Liskov Substitution Principle (LSP)
* Interface Segregation Principle (ISP)
* Dependency Inversion Principle (DIP)

## Entscheidung

Gewählte Variante: "Single Responsibility Principle (SRP)", da wir als Architekturentscheideung das Schichtenmodell gewählt haben, passt SRP perfekt dazu. Wir möchten einen klare Trennung der Verantwortlichkeiten und Funktionalitäten, sodass Codeänderungen nicht an mehreren Stellen passieren müssen und Fehler weitreichend das ganze Projekt beeinflussen. Zudem möchten wir ELemente in der Datenpersistenz und dem Frontend einfach bei Bedarf austauschen können.

## Status

Angenommen

## Konsequenzen

- Wechsel von LSP auf SRP. Da wir keinen Vererbung haben und auch keine Datenlogik mit Vererbung geplant ist ist LSP als Designprinzip sinnfrei
- Einbindung von Service-Dateien für klare Trenneung der Aufgabenbereiche
