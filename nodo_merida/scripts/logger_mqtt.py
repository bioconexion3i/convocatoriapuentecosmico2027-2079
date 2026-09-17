#!/usr/bin/env python3
# logger_mqtt.py - AJUSTE: columna nahual_activado para eventos de vector/oraculo
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
        writer.writerow(["timestamp_iso","timestamp_unix","topic","nodo_id","evento","score_armonia","temperatura","humedad","vibracion","tipo_evento","nahual_es","nahual_activado"])

def on_connect(client, userdata, flags, rc):
    print(f"Conectado con codigo {rc}"); client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        now = datetime.now(); row = [now.isoformat(), int(now.timestamp()), msg.topic]
        if "telemetria" in msg.topic:
            datos = payload.get("telemetria_iot", {})
            row.extend([datos.get("id_nodo","ritual_3i"),"telemetria",payload.get("score_armonia",""),datos.get("temperatura",""),datos.get("humedad",""),datos.get("vibracion",""),"",""])
        elif "evento" in msg.topic:
            nahual_act = ""
            if "nahuales_activos" in payload and payload["nahuales_activos"]:
                nahual_act = payload["nahuales_activos"][0].get("nombre","")
            row.extend([payload.get("nodo_id","ritual_3i"),"evento_ritual","","","","",payload.get("tipo",""),payload.get("nahual",{}).get("es",""),nahual_act])
        else:
            row.extend([payload.get("node","desconocido"),"telemetria_simulada",payload.get("score",""),"","","","",""])
        with open(CSV_PATH, 'a', newline='') as f:
            csv.writer(f).writerow(row)
        print(f"Guardado: {msg.topic}")
    except Exception as e:
        print(f"Error: {e}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect; client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60); client.loop_forever()
