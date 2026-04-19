#!/usr/bin/env python3
# ritual_3i_mqtt.py - Integrador de Telemetría IoT y Sincronía Galáctica
# Nodo Faro Mérida - Red Stardust

import paho.mqtt.client as mqtt
import json
import time
import sys
import signal
from datetime import datetime

# --- IMPORTACIONES DE MÓDULOS DE PROYECTO ---
import reloj_cosmico
from engine_bioconexion import EngineBioconexion 

# ========================= CONFIGURACIÓN =========================
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "ritual_3i_publisher_v2"
PUBLISH_INTERVAL = 30
TOPIC_TELEMETRIA = "stardust/ritual_3i/telemetria"
TOPIC_EVENTO = "stardust/ritual_3i/evento"

# Archivo de nahuales
NAHUALES_JSON = "nahuales_20_universalis.json"

# Inicializar motor de sincronía galáctica
engine = EngineBioconexion()

# ========================= CARGA DE DATOS =========================
def cargar_nahuales():
    try:
        with open(NAHUALES_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "nahuales" in data:
            nahuales_lista = data["nahuales"]
            return [{
                "es": n["keywords"]["es"],
                "en": n["keywords"]["en"],
                "zh": n["keywords"]["zh"]
            } for n in nahuales_lista]
        return None
    except Exception as e:
        print(f"Error cargando {NAHUALES_JSON}: {e}")
        return None

# ========================= NÚCLEO DE INTEGRACIÓN =========================
def obtener_payload_unificado():
    """
    Fusión del Paso 3: Datos físicos + Contexto Arqueoastronómico.
    """
    # 1. Obtener vectores del motor (Cuenta Larga, Venus, Luna, 819 días)
    vectores_cosmicos = engine.compute_all_vectors()
    
    # 2. Simulación/Lectura de sensores físicos
    datos_sensores = {
        "temperatura": 25.3,
        "humedad": 68,
        "vibracion": 0.12,
        "id_nodo": "merida-avenida-yucatan"
    }

    # 3. Construcción del Payload AI-Ready
    return {
        "timestamp": int(time.time()),
        "telemetria_iot": datos_sensores,
        "sincronia_galactica": vectores_cosmicos,
        "score_armonia": vectores_cosmicos["harmony_factor"] # Derivado del Supernúmero 9.9.16.0.0
    }

def publicar_ritual(client, nahual_info, tipo_evento):
    """Publica un evento ritual (Campana de Hunab Ku)."""
    vectores = engine.compute_all_vectors()
    payload = {
        "timestamp": datetime.now().isoformat(),
        "evento": "Hunab_Ku_Signal",
        "tipo": tipo_evento,
        "cuenta_larga": vectores["long_count"],
        "nahual": {
            "es": nahual_info["es"][0] if isinstance(nahual_info["es"], list) else nahual_info["es"],
            "en": nahual_info["en"][0] if isinstance(nahual_info["en"], list) else nahual_info["en"]
        }
    }
    client.publish(TOPIC_EVENTO, json.dumps(payload))
    print(f"🔔 Evento Ritual: {tipo_evento} - {payload['cuenta_larga']}")

# ========================= EJECUCIÓN =========================
def signal_handler(sig, frame):
    print("\n🛑 Nodo Faro Mérida desconectado.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=MQTT_CLIENT_ID)
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        print(f"❌ Error de conexión MQTT: {e}")
        sys.exit(1)

    nahuales = cargar_nahuales()
    print(f"✅ Nodo Faro Mérida activo. Sincronizando con Hunab Ku...")

    try:
        while True:
            # Generar y publicar el payload unificado
            payload = obtener_payload_unificado()
            client.publish(TOPIC_TELEMETRIA, json.dumps(payload))
            print(f"📡 Telemetría Galáctica: {payload['sincronia_galactica']['long_count']} | Score: {payload['score_armonia']}")

            # Lógica ritual basada en reloj_cosmico
            if reloj_cosmico.es_momento_ritual():
                idx = reloj_cosmico.obtener_indice_nahual()
                if nahuales and 0 <= idx < len(nahuales):
                    tipo = "Inicio de Ciclo 819" if payload["sincronia_galactica"]["kawiil_819"]["day"] == 0 else "Pulsar Cuadrante"
                    publicar_ritual(client, nahuales[idx], tipo)

            time.sleep(PUBLISH_INTERVAL)
    except KeyboardInterrupt:
        client.disconnect()
