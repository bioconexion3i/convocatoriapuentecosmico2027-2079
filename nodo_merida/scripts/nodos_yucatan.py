#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.connect("localhost", 1883, 60)

nodos = {
    "sisal/manglares": {"base": 0.7},
    "tekanto/verde": {"base": 0.6},
    "celestun/flamencos": {"base": 0.8}
}

while True:
    for topic, data in nodos.items():
        score = data["base"] + random.uniform(-0.05, 0.05)
        payload = {
            "timestamp": datetime.now().isoformat(),
            "score": round(score, 3),
            "node": topic.replace("/", "_")
        }
        client.publish(f"stardust/{topic}", json.dumps(payload))
    time.sleep(60)
