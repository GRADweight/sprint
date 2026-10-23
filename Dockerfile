# syntax=docker/dockerfile:1
# sprint — ein Prototyp in unter 60 Minuten. Effimer, non-root, kein Host-Netz.
# sprint ist pure Python-Standardbibliothek (null Runtime-Abhängigkeiten),
# darum braucht der Build kein Netz und kein pip.
FROM python:3.11-slim

# App-Datei in ein schreibgeschütztes Layout.
COPY sprint/  /app/sprint/
COPY sandbox/ /app/sandbox/
COPY pyproject.toml /app/

WORKDIR /app
ENV PYTHONPATH=/app

# Effimerer, non-root Container: beim Lauf mit --user nobody, --read-only,
# --network none (siehe README-Schnellstart). Der Container selbst ist klein.
CMD ["python", "-m", "sprint", "run"]
