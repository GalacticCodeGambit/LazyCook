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

Gewählte Variante: "Liskov Substitution Principle (LSP)", denn damit stellen wir sicher, dass sich alle unsere Speicher-Implementierung gegenüber der Geschäftslogik gleich verhalten. Diese Variante, erlaubt uns es die Datenquelle später auszutauschen, ohne den Code im Service ändern zu müssen

## Status

Angenommen

## Konsequenzen

* Gut, weil die Wartbarkeit erhöht wird. 
* Gut, weil die Testbarkeit verbessert wird.
* Schlecht, weil der initiale Entwicklungsaufwand leicht steigt, da wir erst Interfaces definieren müssen, bevor wir die Logik implementieren können.
* Schlecht, weil wir beim Design der Schnittstellen sehr sorgfältig sein müssen, um sicherzustellen, dass zukünftige Implementierungen (z. B. eine API, die Netzwerkfehler werfen kann) das Prinzip nicht verletzen.
