#!/usr/bin/env python3
# vectorizador_nahual_universalis.py - Versión completa con 20 nahuales en 3 idiomas
# Basado en "Observadores del cielo en el México antiguo" de Anthony F. Aveni
# Proyecto Hunab Ku B.6 / Red Stardust

import json
import re
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

class VectorizadorNahualUniversalis:
    def __init__(self, path_json: str = "nahuales_20_universalis.json"):
        with open(path_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.nahuales = data["nahuales"]

    def vectorizar(self, texto: str):
        # Detectar idioma
        try:
            lang = detect(texto[:500])
        except:
            lang = "es"

        # Normalizar clave de idioma
        if lang.startswith('zh'):
            lang_key = 'zh'
        elif lang.startswith('en'):
            lang_key = 'en'
        else:
            lang_key = 'es'

        vector = [0.0] * 128

        if lang_key == 'zh':
            # Para chino: búsqueda de subcadenas (cada palabra clave debe estar contenida)
            for nahual in self.nahuales:
                if lang_key in nahual["keywords"]:
                    for kw in nahual["keywords"][lang_key]:
                        if kw in texto:
                            vector[nahual["id"]] += 1.0
        else:
            # Para español/inglés: tokenizar
            palabras = re.findall(r'\b\w+\b', texto.lower())
            for palabra in palabras:
                for nahual in self.nahuales:
                    if lang_key in nahual["keywords"] and palabra in nahual["keywords"][lang_key]:
                        vector[nahual["id"]] += 1.0

        # Normalización (opcional, dividir por total de palabras o keywords encontradas)
        total_palabras = len(palabras) if lang_key != 'zh' else len([kw for nahual in self.nahuales if lang_key in nahual["keywords"] for kw in nahual["keywords"][lang_key] if kw in texto])
        if total_palabras > 0:
            for i in range(20):
                vector[i] /= total_palabras

        return vector, lang_key

# ---------- PRUEBA ----------
if __name__ == "__main__":
    vec = VectorizadorNahualUniversalis()

    textos = [
        ("es", "El enemigo fue eliminado con un ataque preciso."),
        ("en", "The enemy was eliminated with a precise strike."),
        ("zh", "敌人被精确打击消灭了。")
    ]

    for lang_esp, texto in textos:
        vector, lang_det = vec.vectorizar(texto)
        print(f"🌍 Esperado: {lang_esp} | Detectado: {lang_det}")
        print(f"📝 Texto: {texto}")
        activados = [(vec.nahuales[i]['nombre_maya'], round(vector[i], 3)) for i in range(20) if vector[i] > 0]
        print(f"   Nahuales activados: {activados}")
        print(f"   Vector (primeras 20 dims): {[round(v, 3) for v in vector[:20]]}\n")
