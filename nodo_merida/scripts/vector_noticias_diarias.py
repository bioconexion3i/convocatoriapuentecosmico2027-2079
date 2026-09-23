#!/usr/bin/env python3
"""
Vectoriza noticias diarias y publica en stardust/merida/vector
Ejecutar: 08:00 America/Merida (cron)
"""

import os
import sys
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from vectorizador_nahual import VectorizadorNahualUniversalis
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

NOTICIAS_URL = os.getenv("NOTICIAS_URL", "")
NOTICIAS_API_KEY = os.getenv("NOTICIAS_API_KEY", "")
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER", "merida_pub")
MQTT_PASS = os.getenv("MQTT_PASS", "XXX")

def obtener_noticias_diarias():
    """Obtiene titulares del día"""
    if not NOTICIAS_URL:
        # Fallback: texto hardcoded para prueba
        return "La serpiente de energia cosmica transformo la noche en el centro de Merida"
    
    try:
        resp = requests.get(
            NOTICIAS_URL,
            headers={"Authorization": f"Bearer {NOTICIAS_API_KEY}"},
            params={"date": datetime.now().strftime("%Y-%m-%d"), "limit": 10},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        textos = [item["titulo"] for item in data.get("headlines", [])]
        return " ".join(textos)[:500]
    except Exception as e:
        print(f"[error] {e}")
        return "Noticias no disponibles"

def get_mqtt_client():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    return client

def main():
    texto = obtener_noticias_diarias()
    print(f"[info] Vectorizando: {texto[:80]}...")
    
    vectorizador = VectorizadorNahualUniversalis()
    vector, lang = vectorizador.vectorizar(texto)  # Desempaquetar tupla
    
    # Top 5 nahuales activados
    top5 = sorted([(i, vector[i]) for i in range(len(vector)) if vector[i] > 0], reverse=True)[:5]
    
    # Cargar nahuales para obtener nombres
    with open("nahuales_20_universalis.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    nahuales_map = {n["id"]: n["nombre_maya"] for n in data["nahuales"]}
    
    payload = {
        "texto": texto,
        "idioma": lang,
        "nahuales_activos": [
            {"id": idx, "nombre": nahuales_map.get(idx, f"nahual_{idx}"), "score": float(score)}
            for idx, score in top5
        ],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tipo": "noticias_diarias"
    }
    
    client = get_mqtt_client()
    client.publish("stardust/merida/vector", json.dumps(payload, ensure_ascii=False), qos=1)
    print(f"[mqtt] Publicado: {len(top5)} nahuales")
    client.disconnect()

if __name__ == "__main__":
    main()
