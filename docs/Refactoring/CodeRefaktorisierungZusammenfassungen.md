
# Zusammenfassung der Refaktorisierung

Der *Code des kompletten Backends*, bis auf die Tests, wurde *refaktorisiert*. Dabei wurde der Fokus auf Klassennamen, Methodennamen, Dateinamen, sowie Klassenvariablen gelegt.
<br>
<br>
Ziel der vorgenommenen Refaktorisierung war, dass alle gesetzten Namen zu vereinheitlichen. Für diesen Zweck wurde von dem gesamten Team eine einheitliche Namenskonvention beschlossen:<br>
Alle Namen sollen komplett in **Englisch** mit **UpperCamelCase** definiert werden, um einerseits die **Verständlichkeit** und andererseits die **Wartbarkeit** durch die Vereinheitlichung zu sichern. Ferner werden alle Namen **zusammengeschrieben**, wobei Methoden- und Variablennamen am Anfang *klein geschrieben* sowie Klassen- und Dateinamen *groß geschrieben*  werden.
<br>
<br>
Dieser Regel nach wurde die Backend-Refaktorisierung durchgeführt. Dennoch wurden teilweise temporäre Variablen innerhalb von Methoden noch nicht refaktorisiert, was zukünftig noch angepasst werden muss. Außerdem fand noch keine Refaktorisierung des Frontends statt, welche zeitnah für die weitere Entwicklung erheischt wird.
<br>
<br>
Desweiteren wurden die Backend-Datein klar nach Funktionalität getrennt. Jede Datei speiegelt eine bestimmte Funktion wieder und interagiert mit anderen Dateien über imports. So wurde die ehemalige LazyCookAdministration.py, welche die FastAPI Intitialisierung und Fast-API-Endpunkte bereitgestellt hat, aufgeteilt in LazyCookAdministration.py (Initialisierung) und Routes.py (Endpunkte). Damit wurde die Datei in ihrer Größe und komplexität entzogen und klar funktional getrennt.
<br>
<br>
In einem weiteren Schritt wurden sensible Variablen wie die Anmeldedaten zu unserer Gmail und das Secret für die Authentifizierung in einen .env ausgelagert, so dass sie nicht mehr direkt im Code stehen und damit ein hohes Sicherheitsrisiko darstellen.

