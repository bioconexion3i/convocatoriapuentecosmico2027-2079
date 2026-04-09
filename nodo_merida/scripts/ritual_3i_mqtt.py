#!/usr/bin/env python3
# ritual_3i_mqtt.py - Publica telemetría y eventos rituales

import paho.mqtt.client as mqtt
import json
import time
import sys
import signal
from datetime import datetime
import reloj_cosmico

# ========================= CONFIGURACIÓN =========================
MQTT_BROKER = "192.168.100.35"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "ritual_3i_publisher"
PUBLISH_INTERVAL = 30

# Archivo de nahuales (debe estar en el mismo directorio)
NAHUALES_JSON = "nahuales_20_universalis.json"

# ========================= CARGA DE NAHUALES =========================
def cargar_nahuales():
    try:
        with open(NAHUALES_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "nahuales" in data:
            nahuales_lista = data["nahuales"]
            formato_esperado = []
            for n in nahuales_lista:
                formato_esperado.append({
                    "es": n["keywords"]["es"],
                    "en": n["keywords"]["en"],
                    "zh": n["keywords"]["zh"]
                })
            return formato_esperado
        else:
            print("Error: el JSON de nahuales no tiene el formato esperado.")
            return None
    except Exception as e:
        print(f"Error cargando {NAHUALES_JSON}: {e}")
        return None

# ========================= FUNCIONES AUXILIARES =========================
def obtener_datos_sensores():
    """
    Simulación de lectura de sensores.
    Reemplaza con tu código real.
    """
    return {
        "temperatura": 25.3,
        "humedad": 68,
        "vibracion": 0.12,
        "score_armonia": reloj_cosmico.obtener_resonancia_819()
    }

def publicar_telemetria(client, datos):
    """Publica los datos de telemetría en el tópico principal."""
    payload = {
        "timestamp": int(time.time()),
        "datos": datos
    }
    client.publish("stardust/ritual_3i/telemetria", json.dumps(payload))
    print(f"📡 Telemetría publicada: {payload}")

def publicar_ritual(client, nahual_info, tipo_evento):
    """Publica un evento ritual (Campana de Hunab Ku)."""
    ahora = datetime.now()
    payload = {
        "timestamp": ahora.isoformat(),
        "evento": "Hunab_Ku",
        "tipo": tipo_evento,
        "nahual": {
            "es": nahual_info["es"][0] if isinstance(nahual_info["es"], list) else nahual_info["es"],
            "en": nahual_info["en"][0] if isinstance(nahual_info["en"], list) else nahual_info["en"],
            "zh": nahual_info["zh"][0] if isinstance(nahual_info["zh"], list) else nahual_info["zh"]
        }
    }
    client.publish("stardust/ritual_3i/evento", json.dumps(payload))
    print(f"🔔 Evento ritual publicado: {tipo_evento}")

# ========================= MANEJADOR DE SEÑAL =========================
def signal_handler(sig, frame):
    print("\n🛑 Nodo detenido por el usuario.")
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ========================= EJECUCIÓN PRINCIPAL =========================
if __name__ == "__main__":
    # Inicializar cliente MQTT
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=MQTT_CLIENT_ID)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    # Cargar nahuales
    nahuales = cargar_nahuales()
    if nahuales is None:
        print("❌ No se pudo cargar el archivo de nahuales. El nodo se detendrá.")
        sys.exit(1)

    print("✅ Nodo Faro Mérida iniciado.")
    print(f"📅 Fecha base maya: {reloj_cosmico.FECHA_BASE_MAYA.strftime('%d/%m/%Y')}")

    # Bucle principal
    try:
        while True:
            datos = obtener_datos_sensores()
            publicar_telemetria(client, datos)

            if reloj_cosmico.es_momento_ritual():
                idx = reloj_cosmico.obtener_indice_nahual()
                if nahuales and 0 <= idx < len(nahuales):
                    nahual_info = nahuales[idx]
                    ahora = datetime.now()
                    delta = ahora - reloj_cosmico.FECHA_BASE_MAYA
                    dias = delta.days + delta.seconds / 86400.0
                    cuadrante = round(dias / 204.75)
                    tipo_evento = "Inicio de Ciclo" if cuadrante % 4 == 0 else "Cuadrante"
                    publicar_ritual(client, nahual_info, tipo_evento)

            time.sleep(PUBLISH_INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 Nodo detenido por el usuario.")
        client.disconnect()
        sys.exit(0)
