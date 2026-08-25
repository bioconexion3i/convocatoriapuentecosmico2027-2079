#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ritual 3I - Nodo Faro Mérida
PUENTE ADAPTADO AL MOTOR REAL (2026-08-01)
Motor: engine_bioconexion.py (funciones sueltas)
Estabilidad: parches E-01, M-01, M-02, E-04 + paho-mqtt v2
"""

import json
import logging
import os
import random
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import paho.mqtt.client as mqtt

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
        raise ValueError(f"MQTT_PORT fuera de rango (1-65535): {port}.")
    return port


BROKER_HOST = _get_mqtt_host()
BROKER_PORT = _get_mqtt_port()
CLIENT_ID = f"ritual_3i_{random.randint(1000, 9999)}"
NAHUALES_JSON = Path(__file__).resolve().parent / "nahuales_20_universalis.json"

# Credenciales MQTT (desde variables de entorno)
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")  # gitleaks:allow
TOPIC_TELEMETRIA = "stardust/merida/telemetria"
RITMO_SEGUNDOS = 30
MAYA_GMT_CORRELATION = 584283

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ============================================================
# CARGA DE NAHUALES
# ============================================================
def cargar_nahuales():
    """Carga el archivo de nahuales. Nunca devuelve None."""
    try:
        with NAHUALES_JSON.open("r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)
        if isinstance(data, dict) and "nahuales" in data:
            return data["nahuales"]
        logger.warning("El archivo nahuales.json no tiene la estructura esperada.")
    except FileNotFoundError:
        logger.warning("Archivo nahuales.json no encontrado. Usando lista vacía.")
    except json.JSONDecodeError as exc:
        logger.error("Error decodificando nahuales.json: %s", exc)
    except Exception as exc:
        logger.error("Error inesperado cargando nahuales: %s", exc)
    return []


# ============================================================
# MANEJO DE SEÑALES
# ============================================================
client = None


def signal_handler(sig, frame):
    """Maneja SIGINT y SIGTERM para cerrar limpiamente."""
    del sig, frame
    logger.info("🛑 Ritual detenido por el Guardián.")
    global client
    try:
        if client is not None:
            client.loop_stop()
            if client.is_connected():
                client.disconnect()
            logger.info("Cliente MQTT desconectado con honor.")
    except Exception as exc:
        logger.error("Error al desconectar MQTT: %s", exc)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ============================================================
# PUBLICACIÓN MQTT
# ============================================================
def publicar_ritual(mqtt_client, topic, payload):
    """Publica un mensaje MQTT con manejo de errores."""
    try:
        result = mqtt_client.publish(topic, payload, qos=1)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            return True
        logger.error("Fallo al publicar en %s: código %s", topic, result.rc)
    except Exception as exc:
        logger.error("Excepción publicando en %s: %s", topic, exc)
    return False


# ============================================================
# CONEXIÓN Y RECONEXIÓN
# ============================================================
def crear_cliente():
    """Crea el cliente MQTT usando la API v2 de paho-mqtt."""
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=CLIENT_ID,
    )
    # Inyectar credenciales si existen
    if MQTT_USER and MQTT_PASSWORD:  # gitleaks:allow
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    return client


def conectar_con_reintentos(mqtt_client, max_intentos=None):
    """Conecta al broker con espera progresiva entre intentos."""
    intento = 0
    espera = 2

    while max_intentos is None or intento < max_intentos:
        intento += 1
        try:
            mqtt_client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
            logger.info("Conectado al broker MQTT en %s:%s", BROKER_HOST, BROKER_PORT)
            return True
        except Exception as exc:
            logger.error(
                "Error conectando al broker (intento %s): %s", intento, exc
            )
            if max_intentos is not None and intento >= max_intentos:
                return False
            time.sleep(espera)
            espera = min(espera * 2, 60)
    return False


def asegurar_conexion(mqtt_client):
    """Reintenta la conexión si el broker se desconectó."""
    if mqtt_client.is_connected():
        return True
    logger.warning("Broker MQTT desconectado; iniciando reconexión.")
    return conectar_con_reintentos(mqtt_client)


# ============================================================
# BUCLE PRINCIPAL
# ============================================================
def main_loop():
    global client

    logger.info("🌌 Iniciando Nodo Faro Mérida (Motor Real Activado)...")
    client = crear_cliente()

    if not conectar_con_reintentos(client):
        logger.error("No fue posible conectar al broker MQTT.")
        sys.exit(1)

    client.loop_start()
    nahuales = cargar_nahuales()
    logger.info("✅ %s nahuales cargados. Motor cosmológico activo.", len(nahuales))

    try:
        while True:
            try:
                if not asegurar_conexion(client):
                    time.sleep(10)
                    continue

                cosmos_data = get_bioconexion_state()
                now = datetime.now(timezone.utc)
                jdn = get_jdn(now.year, now.month, now.day)
                maya_day = int(jdn - MAYA_GMT_CORRELATION)

                nahual_del_dia = None
                if nahuales:
                    nahual_del_dia = nahuales[(maya_day + 19) % 20]

                payload_dict = {
                    "timestamp": now.isoformat(),
                    "id_nodo": "merida-avenida-yucatan-orin",
                    "latido": random.randint(60, 80),
                    "engine_bioconexion": cosmos_data,
                    "nahual_del_dia": nahual_del_dia,
                }
                payload = json.dumps(
                    payload_dict,
                    ensure_ascii=False,
                    default=str,
                )

                if publicar_ritual(client, TOPIC_TELEMETRIA, payload):
                    nombre_nahual = (
                        nahual_del_dia.get("nombre_maya")
                        if nahual_del_dia
                        else "N/A"
                    )
                    logger.info(
                        "📡 Latido enviado | Venus: %s | Día Ciclo: %s | Nahual: %s",
                        cosmos_data.get("venus_phase"),
                        cosmos_data.get("grand_cycle_day"),
                        nombre_nahual,
                    )

                time.sleep(RITMO_SEGUNDOS)

            except Exception as exc:
                logger.error("⚠️ Error en ciclo de telemetría: %s", exc)
                time.sleep(10)

    except KeyboardInterrupt:
        logger.info("Interrupción manual detectada.")
    finally:
        logger.info("🧹 Limpiando recursos...")
        if client is not None:
            client.loop_stop()
            if client.is_connected():
                client.disconnect()
        logger.info("✅ Faro detenido correctamente. Ometeotl.")


if __name__ == "__main__":
    main_loop()
