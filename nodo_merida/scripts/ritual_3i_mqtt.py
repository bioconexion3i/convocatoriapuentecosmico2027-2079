import time
import json
import psutil
import paho.mqtt.client as mqtt
from engine_bioconexion import get_bioconexion_state

# --- Configuración MQTT (Blindada) ---
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_USER = "stardust_faro"
MQTT_PASS = "stardust2026" # <--- QWEN: PON AQUÍ LA CONTRASEÑA DE MOSQUITTO

TOPIC_TELEMETRIA = "stardust/ritual_3i/telemetria"

def get_telemetry():
    """Recolecta datos del hardware y del cosmos."""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    # Lectura de temperatura del Jetson
    temp = 0.0
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read()) / 1000.0
    except Exception:
        pass

    bioconexion = get_bioconexion_state()

    payload = {
        "nodo": "merida-avenida-yucatan-orin",
        "timestamp": int(time.time()),
        "system": {
            "cpu_percent": cpu,
            "ram_percent": ram,
            "disk_percent": disk,
            "temp_c": temp
        },
        "cosmos": {
            "sak_tahn_waax": bioconexion
        }
    }
    return payload

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado al Broker MQTT. Faro Mérida activo.")
    else:
        print(f"❌ Error de conexión MQTT. Código: {rc}")

def main():
    client = mqtt.Client(client_id="ritual-3i-merida")
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        print("🌌 Iniciando Ritual 3i...")

        while True:
            data = get_telemetry()
            client.publish(TOPIC_TELEMETRIA, json.dumps(data))
            print(f"📡 Telemetría emitida: Venus [{data['cosmos']['sak_tahn_waax']['venus_phase']}] - CPU [{data['system']['cpu_percent']}%]")
            time.sleep(30)

    except KeyboardInterrupt:
        print("\n🛑 Ritual detenido manualmente.")
    except Exception as e:
        print(f"⚠️ Error en el ritual: {e}")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
