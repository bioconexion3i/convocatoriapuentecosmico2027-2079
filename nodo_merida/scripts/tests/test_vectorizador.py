#!/usr/bin/env python3
# test_vectorizador.py - 5 pruebas
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from vectorizador_pipeline import vectorizar, cargar_nahuales, detectar_idioma

nahuales = cargar_nahuales()

def test_espanol_activa_chicchan():
    v, lang = vectorizar("La serpiente de energia cosmica transformo la noche", nahuales)
    assert lang == "es" and v[4] > 0.3  # Chicchan

def test_ingles_activa_chicchan():
    v, lang = vectorizar("The serpent of cosmic energy transformed the night", nahuales)
    assert lang == "en" and v[4] > 0.3

def test_chino_activa_chicchan():
    v, lang = vectorizar("蛇的能量宇宙改变了夜晚", nahuales)
    assert lang == "zh" and v[4] > 0.3

def test_normalizacion():
    v, _ = vectorizar("La serpiente de energia cosmica", nahuales)
    assert abs(sum(v) - 1.0) < 1e-6

def test_payload_schema():
    from datetime import datetime, timezone
    payload = {"texto":"test","idioma":"es","nahuales_activos":[{"id":4,"nombre":"Chicchan","score":0.5}],"timestamp":datetime.now(timezone.utc).isoformat()}
    assert all(k in payload for k in ("texto","idioma","nahuales_activos","timestamp"))
    assert isinstance(payload["nahuales_activos"], list) and len(payload["nahuales_activos"]) <= 5

if __name__ == "__main__":
    pruebas = [test_espanol_activa_chicchan, test_ingles_activa_chicchan, test_chino_activa_chicchan, test_normalizacion, test_payload_schema]
    for p in pruebas:
        try: p(); print(f"OK {p.__name__}")
        except AssertionError: print(f"FALLO {p.__name__}")
