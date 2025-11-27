# Architekturstil

## Kontext und Problemstellung

Welcher Architekturstil soll für das Projekt verwendet werden? Um eine einheitliche Umsetzung im gesamten Projekt zu gewährleisten, die auch im zeitlich realisierbar ist. 


## Betrachtete Varianten

* Schichtbasierter Architekturstil
* Servicebasierter Architekturstil
* Eventbasierter Architekturstil
* "Space-based" Architekturstil
* Microservices Architekturstil
* MicrokernelArchitekturstil

## Entscheidung

Gewählte Variante: "Schichtbasierter Architekturstil", da diese einfach umzusetzen ist und die Verantwortlichkeiten klar trennt.

## Status

Angenommen

## Konsequenzen

* Gut, weil es einfach und leicht umzusetzen ist. <!--jeder Entwickler weiß wie LazyCook aufgebaut sein soll im Frontend und Backend sowie die Kommunikation zwischen diesen--> 
* Gut, weil es eine klare Trennung der Verantwortlichkeiten vorgibt. 
* Schlecht, weil es weniger Fehlertoleranz gibt.
* Schlecht, da die Skalierbarkeit und Testbarkeit geringe sind.
