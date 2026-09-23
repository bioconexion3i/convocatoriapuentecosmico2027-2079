#!/usr/bin/env python3
"""
Suscribe a stardust/merida/evento y actualiza cache local
"""

import json
import os
import paho.mqtt.client as mqtt
from pathlib import Path
from datetime import datetime

CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "oraculo_hoy.json"

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER", "exar_lector")
MQTT_PASS = os.getenv("MQTT_PASSWORD", "")

def on_connect(client, userdata, flags, rc):
    print(f"[mqtt] Conectado: {rc}")
    if rc == 0:
        client.subscribe("stardust/merida/evento", qos=1)
    else:
        print(f"[error] Error de conexión: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        if payload.get("tipo") == "oraculo_diario":
            payload["_cache_updated"] = datetime.now().isoformat()
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            print(f"[cache] Oráculo actualizado: {payload.get('kin', 'N/A')}")
    except Exception as e:
        print(f"[error] {e}")

def main():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print(f"[info] Suscrito a stardust/merida/evento, usuario={MQTT_USER}, puerto={MQTT_PORT}, cache en {CACHE_FILE}")
    client.loop_forever()

if __name__ == "__main__":
    main()
