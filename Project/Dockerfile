#FROM ubuntu:latest
#ENV DEBIAN_FRONTEND=noninteractive
#
## Kopiere Datei mit den Abhänigkeiten -> um Docker's Caching zu nutzen
##COPY package*.json ./
#
## Installiere die Abhängigkeiten
#RUN #npm install
#
## Kopiere den Rest der Applikation
#COPY . .
#
## Setz Standard-Umgebungsvariablen
#ENV PORT=8000
#
##
#EXPOSE ${PORT}
#
## Starte die Applikation
##CMD ["python3", "app.py"]


# File: Project/Dockerfile  (Backend)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir gunicorn
COPY . /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
# Starte die Flask-App mit Gunicorn für Production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]




#FROM ubuntu:latest
#ENV DEBIAN_FRONTEND=noninteractive
#
## Installiere sqlite (CLI + dev libs) und Python für Entwicklung
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    sqlite3 libsqlite3-dev python3 python3-pip build-essential \
# && rm -rf /var/lib/apt/lists/*
#
## Optional: non-root User für Entwicklung
#RUN useradd -m dev && chown -R dev:dev /home/dev
#USER dev
#WORKDIR /home/dev/app
#
## Projektdateien kopieren / Abhängigkeiten installieren (falls benötigt)
## COPY . /home/dev/app
## RUN pip3 install -r requirements.txt
#
#ENTRYPOINT ["top", "-b"]