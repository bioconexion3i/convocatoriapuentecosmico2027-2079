#!/usr/bin/env python3
# reloj_cosmico.py - Ciclos mayas, resonancia 819 días y nahual actual

from datetime import datetime, timedelta
import json
import os

# Fecha base de referencia para el ciclo de 819 días
# Ajustada al 21 de diciembre de 2012 (13.0.0.0.0) según el proyecto
FECHA_BASE_MAYA = datetime(2012, 12, 21)

# Ruta al archivo de nahuales (asumiendo que está en el mismo directorio)
NAHUALES_JSON = os.path.join(os.path.dirname(__file__), "nahuales_20_universalis.json")

# Cargar nahuales una sola vez al inicio
try:
    with open(NAHUALES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "nahuales" in data:
        NAHUALES = data["nahuales"]
    else:
        NAHUALES = []
        print("Advertencia: No se pudo cargar la lista de nahuales.")
except Exception as e:
    NAHUALES = []
    print(f"Error cargando nahuales: {e}")

def obtener_resonancia_819():
    """
    Calcula la resonancia del ciclo de 819 días.
    Retorna un valor flotante entre 0 y 1 que representa la fase actual del ciclo.
    0 = inicio del ciclo, 1 = final (justo antes del siguiente inicio).
    """
    ahora = datetime.now()
    delta = ahora - FECHA_BASE_MAYA
    dias_desde_base = delta.days + delta.seconds / 86400.0  # incluir fracción de día
    ciclo = 819.0
    fase = (dias_desde_base % ciclo) / ciclo
    return fase  # valor entre 0 y 1

def es_momento_ritual(margen_horas=12):
    """
    Determina si hoy es un punto de armonía máxima:
    - Inicio exacto de un ciclo de 819 días (fase 0)
    - Cuadrantes (cada 204.75 días) con margen.
    Retorna True si está dentro del margen.
    """
    fase = obtener_resonancia_819()
    # Inicio de ciclo
    if fase < 1e-6 or abs(fase - 1.0) < 1e-6:
        return True
    # Cuadrantes: 0.25, 0.5, 0.75
    cuadrantes = [0.25, 0.5, 0.75]
    margen = margen_horas / 24.0 / 819.0  # convertir horas a fracción del ciclo
    for q in cuadrantes:
        if abs(fase - q) <= margen:
            return True
    return False

def obtener_nahual_actual():
    """
    Calcula el nahual del día según el Tzolkin (260 días).
    Retorna un diccionario con el nombre maya, azteca, significado y keywords.
    Si no se pudo cargar la lista, retorna un nahual por defecto.
    """
    # Días desde una fecha base conocida (4 Ajaw). Por simplicidad, usamos el 21/12/2012 como 4 Ajaw.
    # En Tzolkin, el ciclo es de 260 días. Cada día tiene un número (1-13) y un nahual (20).
    # Vamos a calcular el índice del nahual (0-19).
    fecha_base = datetime(2012, 12, 21)  # 13.0.0.0.0, 4 Ajaw
    delta = datetime.now() - fecha_base
    dias = delta.days
    indice_nahual = dias % 20
    if NAHUALES and 0 <= indice_nahual < len(NAHUALES):
        return NAHUALES[indice_nahual]
    else:
        # Nahual por defecto si falla la carga
        return {
            "id": indice_nahual,
            "nombre_maya": "Desconocido",
            "nahual_azteca": "",
            "significado": "",
            "keywords": {"es": [], "en": [], "zh": []}
        }

# Si se ejecuta directamente, muestra una prueba
if __name__ == "__main__":
    print(f"Resonancia 819: {obtener_resonancia_819():.4f}")
    print(f"Es momento ritual: {es_momento_ritual()}")
    nahual = obtener_nahual_actual()
    print(f"Nahual actual: {nahual['nombre_maya']} ({nahual['significado']})")
