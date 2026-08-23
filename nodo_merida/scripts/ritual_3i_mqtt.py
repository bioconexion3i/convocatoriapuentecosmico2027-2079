#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ritual 3I - Nodo Faro Mérida
PUENTE ADAPTADO AL MOTOR REAL (2026-08-01)
Motor: engine_bioconexion.py (funciones sueltas)
Estabilidad: parches E-01, M-01, M-02, E-04 + ajuste paho-mqtt v2
"""

import json
import os
import time
import signal
import sys
import random
from pathlib import Path
import logging
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

# Importar las funciones reales del motor
from engine_bioconexion import get_bioconexion_state, get_jdn

# ============================================================
# CONFIGURACIÓN
# ============================================================
def _get_mqtt_host(environ=None):
    env = environ if environ is not None else os.environ
    return env.get("MQTT_BROKER", "127.0.0.1")


def _get_mqtt_port(environ=None):
    env = environ if environ is not None else os.environ
    raw_port = env.get("MQTT_PORT", "1883")
    try:
        port = int(raw_port)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"MQTT_PORT inválido: {raw_port!r}. Debe ser un entero."
        ) from exc
    if not 1 <= port <= 65535:
        raise ValueError(
            f"MQTT_PORT fuera de rango (1-65535): {port}."
        )
    return port


BROKER_HOST = _get_mqtt_host()
BROKER_PORT = _get_mqtt_port()
CLIENT_ID = f"ritual_3i_{random.randint(1000, 9999)}"
NAHUALES_JSON = Path(__file__).resolve().parent / "nahuales.json"
TOPIC_TELEMETRIA = "stardust/merida/telemetria"
RITMO_SEGUNDOS = 30

# Correlación GMT estándar para el calendario Maya (Cuenta Larga)
MAYA_GMT_CORRELATION = 584283

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# ============================================================
# CARGA DE NAHUALES (Parche E-01)
# ============================================================
def cargar_nahuales():
    """Carga el archivo de nahuales. Nunca devuelve None."""
    try:
        with open(NAHUALES_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict) and "nahuales" in data:
            return data["nahuales"]
        logger.warning("El archivo nahuales.json no tiene la estructura esperada.")
        return []
    except FileNotFoundError:
        logger.warning("Archivo nahuales.json no encontrado. Usando lista vacía.")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Error decodificando nahuales.json: {e}")
        return []
    except Exception as e:
        logger.error(f"Error inesperado cargando nahuales: {e}")
        return []

# ============================================================
# MANEJO DE SEÑALES (Parches M-01 y Z-01)
# ============================================================
client = None

def signal_handler(sig, frame):
    """Maneja SIGINT y SIGTERM para cerrar limpiamente."""
    logger.info("🛑 Ritual detenido por el Guardián.")
    global client
    try:
        if client and client.is_connected():
            client.loop_stop()
            client.disconnect()
            logger.info("Cliente MQTT desconectado con honor.")
    except Exception as e:
        logger.error(f"Error al desconectar MQTT: {e}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ============================================================
# PUBLICACIÓN MQTT (Parche E-04)
# ============================================================
def publicar_ritual(client, topic, payload):
    """Publica un mensaje MQTT con manejo de errores."""
    try:
        result = client.publish(topic, payload, qos=1)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            return True
        logger.error(f"Fallo al publicar en {topic}: código {result.rc}")
        return False
    except Exception as e:
        logger.error(f"Excepción publicando en {topic}: {e}")
        return False

# ============================================================
# BUCLE PRINCIPAL
# ============================================================
def main_loop():
    global client

    logger.info("🌌 Iniciando Nodo Faro Mérida (Motor Real Activado)...")

    # AJUSTE ARQUITECTO: paho-mqtt >= 2.0 requiere CallbackAPIVersion.VERSION1
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=CLIENT_ID)
    try:
        client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
        client.loop_start()
        logger.info(f"Conectado al broker MQTT en {BROKER_HOST}:{BROKER_PORT}")
    except Exception as e:
        logger.error(f"Error conectando al broker MQTT: {e}")
        sys.exit(1)

    # Cargar nahuales
    nahuales = cargar_nahuales()
    logger.info(f"✅ {len(nahuales)} nahuales cargados. Motor cosmológico activo.")

    try:
        while True:
            try:
                # 1. Obtener datos cósmicos reales del motor
                cosmos_data = get_bioconexion_state()
                
                # 2. Calcular Nahual del día
                now = datetime.now(timezone.utc)
                jdn = get_jdn(now.year, now.month, now.day)
                maya_day = int(jdn - MAYA_GMT_CORRELATION)
                
                nahual_del_dia = None
                if nahuales:
                    nahual_del_dia = nahuales[maya_day % 20]

                # 3. Construir payload completo
                payload_dict = {
                    "timestamp": now.isoformat(),
                    "id_nodo": "merida-avenida-yucatan-orin",
                    "latido": random.randint(60, 80), # Simulación de latido vital
                    "engine_bioconexion": cosmos_data,
                    "nahual_del_dia": nahual_del_dia
                }

                payload = json.dumps(payload_dict, ensure_ascii=False, default=str)
                
                if publicar_ritual(client, TOPIC_TELEMETRIA, payload):
                    logger.info(
                        f"📡 Latido enviado | Venus: {cosmos_data.get('venus_phase')} | "
                        f"Día Ciclo: {cosmos_data.get('grand_cycle_day')} | "
                        f"Nahual: {nahual_del_dia.get('nombre_maya') if nahual_del_dia else 'N/A'}"
                    )

                time.sleep(RITMO_SEGUNDOS)

            except Exception as e:
                logger.error(f"⚠️ Error en ciclo de telemetría: {e}")
                time.sleep(10)

    except KeyboardInterrupt:
        logger.info("Interrupción manual detectada.")
    finally:
        logger.info("🧹 Limpiando recursos...")
        if client and client.is_connected():
            client.loop_stop()
            client.disconnect()
        logger.info("✅ Faro detenido correctamente. Ometeotl.")

if __name__ == "__main__":
    main_loop()
