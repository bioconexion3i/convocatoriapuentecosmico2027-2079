#!/usr/bin/env python3
# verify_oracle_delivery.py - Validacion de entrega del Oraculo (aporte Kimi 3)
import argparse
import json
import sys
import time
from datetime import datetime, timezone, timedelta
import paho.mqtt.client as mqtt

TOPIC = "stardust/merida/evento"
REQUIRED_FIELDS = {"kin":str,"haab":str,"cuenta_larga":str,"don":str,"sombra":str,"ofrenda":str,"fecha":str,"tipo":str,"nodo_id":str}
TIMEZONE = timezone(timedelta(hours=-6))

class OracleVerifier:
    def __init__(self, broker, user, password, timeout=10):
        self.broker = broker; self.user = user; self.password = password; self.timeout = timeout; self.payload = None
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0: client.subscribe(TOPIC)
        else: print(f"[FAIL] Conexion rechazada: {rc}", file=sys.stderr); sys.exit(1)
    def on_message(self, client, userdata, msg):
        try: self.payload = json.loads(msg.payload.decode("utf-8")); client.disconnect()
        except json.JSONDecodeError as e: print(f"[FAIL] JSON invalido: {e}", file=sys.stderr); client.disconnect(); sys.exit(1)
    def verify(self):
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2); client.username_pw_set(self.user, self.password)
        client.on_connect = self.on_connect; client.on_message = self.on_message
        try: client.connect(self.broker, 1883, 60)
        except Exception as e: print(f"[FAIL] No conecta: {e}", file=sys.stderr); return False
        client.loop_start(); deadline = time.time() + self.timeout
        while time.time() < deadline and self.payload is None: time.sleep(0.1)
        client.loop_stop()
        if self.payload is None: print("[FAIL] Timeout sin mensaje", file=sys.stderr); return False
        errors = []
        for field, t in REQUIRED_FIELDS.items():
            if field not in self.payload: errors.append(f"Falta '{field}'")
            elif not isinstance(self.payload[field], t): errors.append(f"Tipo incorrecto en '{field}'")
        if "fecha" in self.payload:
            try:
                msg_date = datetime.fromisoformat(self.payload["fecha"].replace("Z","+00:00"))
                if msg_date.date() != datetime.now(TIMEZONE).date(): errors.append(f"Fecha desfasada: {msg_date.date()}")
            except Exception as e: errors.append(f"Fecha malformada: {e}")
        if self.payload.get("tipo") != "oraculo_diario": errors.append("tipo != oraculo_diario")
        if errors:
            for e in errors: print(f"[FAIL] {e}", file=sys.stderr)
            return False
        print("[PASS] Oraculo entregado y validado"); return True

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--broker",default="localhost"); ap.add_argument("--user",required=True); ap.add_argument("--pass",dest="password",required=True); ap.add_argument("--timeout",type=int,default=10)
    args = ap.parse_args()
    v = OracleVerifier(args.broker, args.user, args.password, args.timeout)
    sys.exit(0 if v.verify() else 1)

if __name__ == "__main__": main()
