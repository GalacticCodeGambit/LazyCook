# AD01: Sichere Passwortspeicherung in der Datenbank via Hash & Salt

## Kontext und Problemstellung

Bei der Registrierung bei LazyCook werden E-Mail und Passwort des Nutzers erfasst und in einer Datenbank gespeichert. Zur Sicherung der gespeicherten Daten und zum Schutz des Kontos darf das Passwort nicht im Klartext in der Datenbank abgelegt werden. Es stellt sich die Frage wie das Passwort verschlüsselt und in der Datenbank gespeichert werden soll. Das Hash-Verfahren kann bei Unsicherheit vom Entwickler geändert werden.


## Betrachtete Varianten

* SHA256
* SHA256 mit Salt
* PBKDF2-HMAC mit SHA256

## Entscheidung

Gewählte Variante: PBKDF2-HMAC mit SHA256, denn diese ist im Vergleich zu SHA256 und SHA256 mit Salt wesentlich sicherer. SHA256 kann mit den heutigen Grafikkarten sehr schnell berechnet werden. PBKDF2-HMAC mit SHA256 berechnet den Hashwert tausende male, wodurch es für Angreifer sehr schwer ist diesen mit BruteForce zu berechnen. Zudem wird ein Salt verwendet und sie ist gegen Rainbow-Tables abgesichert. Des Weiteren wird dieses Verfahren von der python eigenen hashlib-Bibliothek unterstützt. Gespeichert wird das gehashte Passwort und der Salt mit base64.

## Status

Angenommen

## Konsequenzen

* Gut, weil die Sicherheit der Daten damit garantiert ist und das Passwort nicht im Klartext, sondern entsprechend fester Standards verschlüsselt wurde
* Der Passwortvergleich bei Anmeldung ist dadurch etwas komplexer. Das Salt muss aus der Datenbank abgefragt werden und das eingegebene Passwort muss mit diesem gehasht werden und mit dem gespeicherten Passwort verglichen werden. Es kann in der Bibliothek auch auf ein anderes Hash-Verfahren zugegriffen werden. 

