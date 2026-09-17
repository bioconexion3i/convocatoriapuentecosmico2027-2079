#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vectorizador de nahuales: texto -> vector 20D -> MQTT."""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

NAHUALES_JSON = Path(__file__).parent / "nahuales_20_universalis.json"

def cargar_nahuales():
    with NAHUALES_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)["nahuales"]

def detectar_idioma(texto):
    if sum(1 for c in texto if '\u4e00' <= c <= '\u9fff') > 3:
        return 'zh'
    en_words = {'the','was','with','and','for','enemy','kill','attack','death','serpent','energy'}
    if len(set(re.findall(r'\b\w+\b', texto.lower())) & en_words) >= 2:
        return 'en'
    return 'es'

def vectorizar(texto, nahuales):
    lang = detectar_idioma(texto)
    vector = [0.0] * 20
    if lang == 'zh':
        for n in nahuales:
            for kw in n.get("keywords", {}).get("zh", []):
                if kw in texto:
                    vector[n["id"]] += 1.0
    else:
        palabras = set(re.findall(r'\b\w+\b', texto.lower()))
        for n in nahuales:
            for kw in n.get("keywords", {}).get(lang, []):
                if kw in palabras:
                    vector[n["id"]] += 1.0
    total = sum(vector)
    if total > 0:
        vector = [v / total for v in vector]
    return vector, lang

def publicar_mqtt(payload, topic):
    try:
        import paho.mqtt.client as mqtt
    except ImportError:
        print("[mqtt] paho-mqtt no instalado", file=sys.stderr); return False
    try:
        c = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="vectorizador")
        u, p = os.environ.get("MQTT_USER",""), os.environ.get("MQTT_PASSWORD","")
        if u and p: c.username_pw_set(u, p)
        c.connect(os.environ.get("MQTT_BROKER","127.0.0.1"), int(os.environ.get("MQTT_PORT","1883")), 60)
        c.loop_start(); info = c.publish(topic, json.dumps(payload, ensure_ascii=False), qos=1)
        info.wait_for_publish(timeout=10); c.loop_stop(); c.disconnect()
        return info.rc == 0
    except Exception as e:
        print("[mqtt] error: {}".format(e), file=sys.stderr); return False

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--texto"); ap.add_argument("--archivo")
    ap.add_argument("--topic", default="stardust/merida/vector"); args = ap.parse_args()
    if not args.texto and not args.archivo:
        print("Usa --texto o --archivo", file=sys.stderr); sys.exit(1)
    texto = args.texto if args.texto else Path(args.archivo).read_text(encoding="utf-8")
    nahuales = cargar_nahuales(); vector, lang = vectorizar(texto, nahuales)
    top5 = sorted([(i, vector[i]) for i in range(20) if vector[i] > 0], key=lambda x: x[1], reverse=True)[:5]
    payload = {"texto": texto[:200], "idioma": lang, "nahuales_activos": [{"id":i,"nombre":nahuales[i]["nombre_maya"],"score":s} for i,s in top5], "timestamp": datetime.now(timezone.utc).isoformat()}
    ok = publicar_mqtt(payload, args.topic)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("[mqtt] {}".format("publicado" if ok else "omitido"))

if __name__ == "__main__":
    main()
