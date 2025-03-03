# Usa un'immagine Python aggiornata
FROM python:3.12-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file necessari
COPY app.py requirements.txt ./

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Comando di avvio
CMD ["python", "app.py"]
