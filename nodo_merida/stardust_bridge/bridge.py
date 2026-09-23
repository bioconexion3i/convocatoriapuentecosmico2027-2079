"""
Stardust Bridge — Nodo Faro Mérida
Extiende el proxy original a Ollama con dos endpoints nuevos:
  GET /oraculo/hoy         -> lee oraculo_dia/salida/YYYY-MM-DD.json
  GET /oraculo/{fecha}     -> lee oraculo_dia/salida/{fecha}.json
  GET /telemetria/latest   -> ultimo payload MQTT de stardust/merida/telemetria
Mantiene el proxy POST /api/chat a Ollama.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import httpx
import paho.mqtt.client as mqtt
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")

MQTT_BROKER = os.getenv("MQTT_BROKER", "host.docker.internal")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1884"))
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_TOPIC_TELEMETRIA = os.getenv("MQTT_TOPIC_TELEMETRIA", "stardust/merida/telemetria")

SALIDA_DIR = Path(os.getenv("ORACULO_SALIDA", "/data/oraculo"))
TZ = ZoneInfo(os.getenv("TZ", "America/Merida"))

# ---------------------------------------------------------------------------
# Estado en memoria para la telemetría
# ---------------------------------------------------------------------------
class TelemetriaState:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._payload: dict | None = None
        self._recibido: str | None = None
        self._topic: str | None = None
        self._connected = False
        self._last_error: str | None = None

    def set_conectado(self, valor: bool, error: str | None = None) -> None:
        with self._lock:
            self._connected = valor
            self._last_error = error

    def set_payload(self, topic: str, payload: dict, recibido: str) -> None:
        with self._lock:
            self._topic = topic
            self._payload = payload
            self._recibido = recibido

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "connected": self._connected,
                "last_error": self._last_error,
                "topic": self._topic,
                "recibido": self._recibido,
                "payload": self._payload,
            }


telemetria = TelemetriaState()


# ---------------------------------------------------------------------------
# Cliente MQTT
# ---------------------------------------------------------------------------
def _on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        telemetria.set_conectado(True)
        client.subscribe(MQTT_TOPIC_TELEMETRIA, qos=1)
        print(f"[bridge] MQTT conectado, suscrito a {MQTT_TOPIC_TELEMETRIA}", flush=True)
    else:
        telemetria.set_conectado(False, f"rc={rc}")
        print(f"[bridge] MQTT connect falló: rc={rc}", flush=True)


def _on_disconnect(client, userdata, flags, rc, properties=None):
    telemetria.set_conectado(False, f"disconnect rc={rc}")
    print(f"[bridge] MQTT desconectado: rc={rc}", flush=True)


def _on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
    except Exception as exc:
        print(f"[bridge] payload inválido en {msg.topic}: {exc}", flush=True)
        return
    recibido = datetime.now(TZ).isoformat()
    telemetria.set_payload(msg.topic, payload, recibido)
    print(f"[bridge] telemetría actualizada desde {msg.topic}", flush=True)


def _start_mqtt() -> mqtt.Client:
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="stardust_bridge_lector",
        clean_session=True,
    )
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_connect = _on_connect
    client.on_disconnect = _on_disconnect
    client.on_message = _on_message
    client.connect_async(MQTT_BROKER, MQTT_PORT, keepalive=30)
    client.loop_start()
    return client


# ---------------------------------------------------------------------------
# FastAPI
# ---------------------------------------------------------------------------
app = FastAPI(title="Stardust Bridge", version="2.0")
_mqtt_client: mqtt.Client | None = None


@app.on_event("startup")
async def _startup():
    global _mqtt_client
    _mqtt_client = _start_mqtt()


@app.on_event("shutdown")
async def _shutdown():
    if _mqtt_client is not None:
        _mqtt_client.loop_stop()
        _mqtt_client.disconnect()


# -------------------------- Proxy a Ollama (existente) ---------------------
@app.post("/api/chat")
async def chat_proxy(request: Request):
    data = await request.json()
    if "model" not in data:
        return JSONResponse(status_code=400, content={"error": "Modelo no especificado"})
    data["stream"] = False
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(f"{OLLAMA_HOST}/api/chat", json=data)
            return response.json()
    except httpx.RequestError:
        app.logger.exception("Error de conexión con Ollama")
        return JSONResponse(status_code=500, content={"error": "Error de conexión con Ollama"})
    except Exception:
        app.logger.exception("Error procesando la respuesta de Ollama")
        return JSONResponse(status_code=500, content={"error": "Error interno procesando la respuesta"})


# -------------------------- Oráculo ----------------------------------------
def _leer_oraculo(fecha_iso: str) -> dict:
    archivo = SALIDA_DIR / f"{fecha_iso}.json"
    if not archivo.is_file():
        raise HTTPException(status_code=404, detail=f"Oráculo no encontrado para {fecha_iso}")
    try:
        with archivo.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"JSON inválido: {exc}")


@app.get("/oraculo/hoy")
async def oraculo_hoy():
    hoy = datetime.now(TZ).date().isoformat()
    return JSONResponse(_leer_oraculo(hoy))


@app.get("/oraculo/{fecha}")
async def oraculo_fecha(fecha: str):
    # Espera formato YYYY-MM-DD
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD.")
    return JSONResponse(_leer_oraculo(fecha))


# -------------------------- Telemetría -------------------------------------
@app.get("/telemetria/latest")
async def telemetria_latest():
    snap = telemetria.snapshot()
    if snap["payload"] is None:
        raise HTTPException(status_code=404, detail="Sin telemetría recibida todavía")
    return JSONResponse(snap)


# -------------------------- Health -----------------------------------------
@app.get("/health")
async def health_check():
    snap = telemetria.snapshot()
    return {
        "status": "Stardust Bridge activo y en línea. In lak'ech.",
        "mqtt_connected": snap["connected"],
        "mqtt_last_error": snap["last_error"],
        "telemetria_recibida": snap["recibido"],
        "oraculo_dir": str(SALIDA_DIR),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)
