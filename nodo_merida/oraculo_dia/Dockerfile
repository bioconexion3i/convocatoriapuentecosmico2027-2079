# Oraculo del Dia - Nodo Faro Merida (Red Stardust)
# Contexto de build: nodo_merida/ (ver docker-compose.yml)
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir paho-mqtt==2.1.0
COPY scripts/engine_bioconexion.py scripts/oraculo_del_dia.py ./
ENV TZ=America/Merida ORACLE_HOUR=6 MQTT_BROKER=host.docker.internal MQTT_PORT=1884
VOLUME ["/data"]
CMD ["sh","-c","python oraculo_del_dia.py --hoy --out /data --loop --hora ${ORACLE_HOUR}"]
