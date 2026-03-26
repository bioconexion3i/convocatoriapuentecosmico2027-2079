#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nodo Faro Mérida - Red Stardust
Publica telemetría y eventos rituales (Hunab Ku) cada 30 segundos.
Integra ciclo maya de 819 días y nahuales multi-idioma.
"""

import json
import time
import os
import signal
import sys
from datetime import datetime

import paho.mqtt.client as mqtt

# Módulos locales
import reloj_cosmico  # contiene FECHA_BASE_MAYA, obtener_resonancia_819, es_momento_ritual, obtener_indice_nahual

# ========================= CONFIGURACIÓN =========================
# Configuración MQTT (cambia según tu broker)
MQTT_BROKER = "localhost"      # o tu broker remoto
MQTT_PORT = 1883
MQTT_TOPIC_TELEMETRY = "stardust/merida/telemetria"
MQTT_TOPIC_RITUAL = "stardust/merida/ritual/hunab_ku"
MQTT_CLIENT_ID = "NodoFaroMerida"

# Intervalo de publicación (segundos)
PUBLISH_INTERVAL = 30

# Archivo de nahuales (debe estar en el mismo directorio)
NAHUALES_JSON = "nahuales_20_universalis.json"

# ========================= CARGA DE NAHUALES =========================
def cargar_nahuales():
    """Carga el archivo JSON con los 20 nahuales en tres idiomas."""
    try:
        with open(NAHUALES_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Se espera una lista de objetos con claves "es", "en", "zh"
        if isinstance(data, list) and len(data) == 20:
            return data
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
    Reemplaza con tu código real (temperatura, humedad, vibración, etc.)
    """
    # Aquí puedes integrar tus lecturas reales (por ejemplo, sensores DHT, acelerómetro, etc.)
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
    client.publish(MQTT_TOPIC_TELEMETRY, json.dumps(payload), qos=1)
    print(f"📡 Telemetría enviada: {datos}")

def publicar_ritual(client, nahual_info, tipo_evento):
    """Publica el evento de la Campana Hunab Ku."""
    payload_ritual = {
        "evento": "CAMPANA_HUNAB_KU",
        "tipo": tipo_evento,
        "nahual": {
            "es": nahual_info["es"],
            "en": nahual_info["en"],
            "zh": nahual_info["zh"]
        },
        "vibracion_total": 1.0,
        "mensaje": "Sincronía detectada en el Nodo Faro Mérida"
    }
    client.publish(MQTT_TOPIC_RITUAL, json.dumps(payload_ritual), qos=2)
    print(f"🔔 ¡Campana Hunab Ku! Nahual: {nahual_info['es']} ({tipo_evento})")

# ========================= MANEJADOR DE SEÑAL =========================
def signal_handler(sig, frame):
    print("\n🛑 Nodo detenido por el usuario.")
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ========================= CONEXIÓN MQTT =========================
client = mqtt.Client(MQTT_CLIENT_ID)
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()  # hilo en segundo plano para mantener la conexión

# ========================= CARGA DE DATOS =========================
nahuales = cargar_nahuales()
if nahuales is None:
    print("❌ No se pudo cargar el archivo de nahuales. El nodo se detendrá.")
    sys.exit(1)

print("✅ Nodo Faro Mérida iniciado.")
print(f"📅 Fecha base maya: {reloj_cosmico.FECHA_BASE_MAYA.strftime('%d/%m/%Y')}")

# ========================= BUCLE PRINCIPAL =========================
while True:
    try:
        # 1. Obtener datos de sensores (reemplaza con tu hardware)
        datos = obtener_datos_sensores()

        # 2. Publicar telemetría normal
        publicar_telemetria(client, datos)

        # 3. Verificar si es momento ritual (Hunab Ku)
        if reloj_cosmico.es_momento_ritual():
            # Obtener índice del nahual actual (0-19)
            idx = reloj_cosmico.obtener_indice_nahual()
            nahual_info = nahuales[idx]

            # Determinar el tipo de evento (inicio de ciclo o cuadrante)
            ahora = datetime.now()
            delta = ahora - reloj_cosmico.FECHA_BASE_MAYA
            dias = delta.days + delta.seconds / 86400.0
            cuadrante = round(dias / 204.75)
            tipo_evento = "Inicio de Ciclo" if cuadrante % 4 == 0 else "Cuadrante"

            # Publicar el evento ritual
            publicar_ritual(client, nahual_info, tipo_evento)

        # Esperar hasta el próximo ciclo
        time.sleep(PUBLISH_INTERVAL)

    except Exception as e:
        print(f"⚠️ Error en el bucle principal: {e}")
        time.sleep(5)
