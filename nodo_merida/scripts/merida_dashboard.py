#!/usr/bin/env python3
import os
import asyncio
import json
import subprocess
from datetime import datetime
import jetson_stats
import paho.mqtt.client as mqtt


# --- CONFIG ---
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "stardust/nodo_merida/dashboard"
NODE_ID = "merida-avenida-yucatan-orin"


# --- JETSON MONITORING ---
def get_jetson_stats():
    j = jetson_stats.load()
    cpu = j.cpu["CPU1"]  # or walk all CPUs, it's up to you
    gpu = j.gpu["GPU"]
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "node_id": NODE_ID,
        "stats": {
            "cpu": {
                "usage_pct": sum([c["usage"] for c in j.cpu.values()]) / len(j.cpu),
                "temps": {k: v["temp"]["avg"] for k, v in j.cpu.items()},
                "mhz": sum([c["mhz"] for c in j.cpu.values()]) / len(j.cpu),
            },
            "gpu": {
                "usage_pct": gpu["usage"],
                "temp": gpu["temp"]["avg"],
                "mhz": gpu["mhz"],
            },
            "memory": {
                "total": j.memory["RAM"]["total"],
                "used": j.memory["RAM"]["used"],
                "available": j.memory["RAM"]["available"],
            },
            "temp": {
                "module": j.temperature["GPU"]["value"],
            },
        },
    }


# --- SYSTEMD SERVICES STATUS ---
def get_services_status():
    services = ["mosquitto", "ritual_3i", "cosmograma", "nodos_yucatan", "docker", "ollama"]
    status = {}
    for svc in services:
        try:
            result = subprocess.run(
                ["systemctl", "is-active", svc],
                capture_output=True,
                text=True,
                timeout=3,
            )
            status[svc] = result.stdout.strip()
        except subprocess.TimeoutExpired:
            status[svc] = "timeout"
        except:
            status[svc] = "error"
    return status


# --- MQTT CALLBACKS ---
def on_connect(client, userdata, flags, rc):
    print(f"MQTT connected with code {rc}")
    # Subscribe to broker metrics topics (if using mosquitto-dashboard pattern)
    # client.subscribe("mosquitto/+/metrics/#")


async def publish_dashboard_loop(client):
    while True:
        # 1. Jetson stats
        jetson_data = get_jetson_stats()
        # 2. Services
        jetson_data["systemd"] = get_services_status()
        # 3. Publish to dashboard topic
        payload = json.dumps(jetson_data, indent=2)
        print("Publishing dashboard update...")
        client.publish(MQTT_TOPIC, payload)
        await asyncio.sleep(2.0)  # every 2 seconds


def main():
    # MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)

    # Run forever
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(publish_dashboard_loop(client))
    client.loop_start()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Stopping dashboard...")
    finally:
        client.loop_stop()


if __name__ == "__main__":
    main()
