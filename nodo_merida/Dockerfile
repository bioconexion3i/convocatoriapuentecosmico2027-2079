FROM python:3.9-slim

WORKDIR /app

# Copiar dependencias y scripts
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ .

# Ejecutar el integrador galáctico
CMD ["python", "ritual_3i_mqtt.py"]
