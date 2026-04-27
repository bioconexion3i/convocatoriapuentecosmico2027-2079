#!/usr/bin/env python3
# logger_mqtt.py - Suscribe a stardust/# y guarda en CSV

import paho.mqtt.client as mqtt
import json
import csv
import os
from datetime import datetime

MQTT_BROKER = "192.168.100.35"
MQTT_PORT = 1883
TOPIC = "stardust/#"
CSV_PATH = "../data/yucatan_scores.csv"
os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

if not os.path.isfile(CSV_PATH):
    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp_iso", "timestamp_unix", "topic",
            "nodo_id", "evento", "score_armonia", "temperatura",
            "humedad", "vibracion", "tipo_evento", "nahual_es"
        ])

def on_connect(client, userdata, flags, rc):
    print(f"✅ Conectado a MQTT con código {rc}")
    client.subscribe(TOPIC)
    print(f"📡 Suscrito a {TOPIC}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        now = datetime.now()
        timestamp_iso = now.isoformat()
        timestamp_unix = int(now.timestamp())
        topic = msg.topic
        row = [timestamp_iso, timestamp_unix, topic]

        if "telemetria" in topic:
            # Extraer del formato real
            datos_iot = payload.get("telemetria_iot", {})
            score = payload.get("score_armonia", "")
            row.extend([
                datos_iot.get("id_nodo", "ritual_3i"),
                "telemetria",
                score,
                datos_iot.get("temperatura", ""),
                datos_iot.get("humedad", ""),
                datos_iot.get("vibracion", ""),
                "",
                ""
            ])
        elif "evento" in topic:
            row.extend([
                payload.get("nodo_id", "ritual_3i"),
                "evento_ritual",
                "",
                "",
                "",
                "",
                payload.get("tipo", ""),
                payload.get("nahual", {}).get("es", "")
            ])
        else:
            # Para nodos simulados (formato: {timestamp, score, node})
            row.extend([
                payload.get("node", "desconocido"),
                "telemetria_simulada",
                payload.get("score", ""),      # score va a la columna score_armonia
                "",                            # temperatura
                "",                            # humedad
                "",                            # vibracion
                "",
                ""
            ])

        with open(CSV_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)

        print(f"📝 Guardado: {topic} | Score: {row[5]}")

    except Exception as e:
        print(f"⚠️ Error procesando mensaje: {e}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
