#!/usr/bin/env python3
# ritual_3i_mqtt.py - Versión con consciencia nahual y calendario cenital
# Cálculo dinámico del Tzolk'in usando correlación GMT
# Fase 2 - Red Stardust / Hunab Ku B.6

import paho.mqtt.client as mqtt
import json
from datetime import datetime, date
import time
import reloj_cosmico
# Configuración MQTT
BROKER = "localhost"
PUERTO = 1883
TOPIC_RITUAL = "stardust/ritual"
TOPIC_AUDIT = "stardust/b6/audit"

# Fechas de pasos cenitales en Copán (según Aveni, p. 313)
PASOS_CENITALES = [
    (4, 30),   # 30 de abril
    (8, 13)    # 13 de agosto
]

# -------------------------------------------------------------------
# Funciones de conversión de fecha a día juliano y Tzolk'in
# Basadas en correlación GMT (584283) y fórmulas de Jean Meeus
# -------------------------------------------------------------------

def gregorian_to_jd(year: int, month: int, day: int) -> float:
    """
    Convierte una fecha gregoriana a día juliano astronómico.
    Fórmula válida para años después de 1582 (calendario gregoriano).
    Para años anteriores, se asume gregoriano proléptico.
    """
    if month <= 2:
        year -= 1
        month += 12
    A = year // 100
    B = 2 - A + A // 4
    JD = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    return JD

def obtener_nahual_actual() -> str:
    """
    Calcula el nahual del día actual (número y nombre) basado en la correlación GMT.
    La fecha cero 0.0.0.0.0 corresponde al 11 de agosto de 3114 a.C. (juliano = 584283)
    y es 4 Ahau en el Tzolk'in.
    """
    hoy = date.today()
    jd_hoy = gregorian_to_jd(hoy.year, hoy.month, hoy.day)
    
    # Constante de correlación GMT: día juliano de 0.0.0.0.0
    JD_CERO = 584283.0
    
    # Días transcurridos desde la creación
    dias_desde_cero = int(jd_hoy - JD_CERO)
    
    # Posición en el ciclo de 260 días (Tzolk'in)
    pos = dias_desde_cero % 260
    
    # Lista de nombres de días en orden maya
    nombres = [
        "Imix", "Ik", "Akbal", "Kan", "Chicchán", "Cimí", "Manik", "Lamat", "Muluc", "Oc",
        "Chuen", "Eb", "Ben", "Ix", "Men", "Cib", "Cabán", "Etz'nab", "Cauac", "Ahau"
    ]
    
    # El día cero (pos=0) es 4 Ahau. Ajustamos índices:
    # - Número: (pos + 3) % 13 + 1  (porque 0 → 4)
    # - Nombre: (pos + 19) % 20     (porque Ahau es índice 19)
    numero = ((pos + 3) % 13) + 1
    nombre = nombres[(pos + 19) % 20]
    
    return f"{numero} {nombre}"

def dias_hasta_proximo_cenit():
    """
    Calcula la fecha y días restantes hasta el próximo paso del Sol por el cenit en Copán.
    """
    hoy = datetime.now()
    año_actual = hoy.year
    proximos = []
    
    for mes, dia in PASOS_CENITALES:
        fecha_evento = datetime(año_actual, mes, dia)
        if fecha_evento < hoy:
            # Si ya pasó este año, considerar el próximo año
            fecha_evento = datetime(año_actual + 1, mes, dia)
        delta = fecha_evento - hoy
        proximos.append((fecha_evento, delta.days))
    
    # Elegir el más próximo
    proximo_cenit = min(proximos, key=lambda x: x[1])
    return proximo_cenit[0], proximo_cenit[1]

# -------------------------------------------------------------------
# Bucle principal (se ejecutará cada 5 minutos)
# -------------------------------------------------------------------
def main():
    cliente = mqtt.Client()
    cliente.connect(BROKER, PUERTO, 60)
    
    while True:
        # Calcular próximo cenit
        fecha_cenit, dias_restantes = dias_hasta_proximo_cenit()
        
        # Obtener nahual actual
        nahual_hoy = obtener_nahual_actual()
        
        # Crear payload
        payload = {
            "timestamp": datetime.now().isoformat(),
            "evento": "ritual_3i",
            "proximo_cenit": fecha_cenit.strftime("%Y-%m-%d"),
            "dias_hasta_cenit": dias_restantes,
            "nahual_del_dia": nahual_hoy,
            "mensaje": f"Faltan {dias_restantes} días para el próximo paso cenital en Copán. Hoy es {nahual_hoy}."
        }
        
        # Publicar
        cliente.publish(TOPIC_RITUAL, json.dumps(payload))
        print(f"📡 Publicado: {payload}")
        
        # Esperar 5 minutos antes de la siguiente publicación
        time.sleep(300)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Ritual detenido por el Guardián.")
