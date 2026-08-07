# CTOAi-Funnel - obraz produkcyjny (Python stdlib, zero zaleznosci).
FROM python:3.11-slim

WORKDIR /app
COPY . /app

# Wolumen na leady (trwale mimo restartu kontenera).
RUN mkdir -p /data
VOLUME ["/data"]

EXPOSE 8080
CMD ["python", "server.py"]
