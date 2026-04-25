# soe_core_launcher.py - Núcleo del Sistema Operativo Ecológico
# Integra: EngineBioconexion (ciclos mayas) + MQTT (telemetría/ritual) + Nahuales
# Basado en contexto [1] del repositorio Puente Cósmico 2025-2079

import json
import time
import signal
import sys
import math
from datetime import datetime

# ========================= CONSTANTES Y CONFIGURACIÓN =========================
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
NAHUALES_JSON = "nahuales_20_universalis.json"
INTERVALO_PUBLICACION = 15 * 60  # 15 minutos
ARCHIVO_REGISTRO = "casos_monitoreados.md"

# ========================= ENGINE DE BIOCONEXIÓN (Ciclos Mayas) =========================
class EngineBioconexion:
    def __init__(self):
        self.GMT_CORRELATION = 584283
        self.SUPERNUMBER = 1366560
        self.LUNAR_CYCLE = 29.530588
        self.VENUS_CYCLE = 583.92
        self.CYCLE_819 = 819
        self.LUNAR_BASE = datetime(2022, 12, 23)
        self.VENUS_BASE_JDN = 2460169.5

    def get_jdn(self, date_obj):
        return (date_obj.timestamp() / 86400) + 2440587.5

    def compute_all_vectors(self, target_date=None):
        if target_date is None:
            target_date = datetime.now()
        jdn = self.get_jdn(target_date)
        dias_desde_base = (target_date - self.LUNAR_BASE).days
        ciclo_lunar = dias_desde_base % self.LUNAR_CYCLE
        ciclo_venus = (jdn - self.VENUS_BASE_JDN) % self.VENUS_CYCLE
        ciclo_819 = (jdn - self.LUNAR_BASE.toordinal()) % self.CYCLE_819
        return {
            "jdn": jdn,
            "ciclo_lunar": round(ciclo_lunar, 2),
            "ciclo_venus": round(ciclo_venus, 2),
            "ciclo_819": int(ciclo_819)
        }

# ========================= FUNCIONES AUXILIARES (del contexto [1]) =========================
def detectar_anomalias_humedad(df_humedad):
    """Detecta anomalías en humedad del suelo usando rangos predefinidos [1]."""
    df_humedad['anomalia'] = (df_humedad['humedad'] < 10) | (df_humedad['humedad'] > 90)
    return df_humedad

def registrar_caso(titulo, tipo_alerta, disparador, contexto, respuesta, resolucion, responsable):
    """Registra un caso monitoreado siguiendo el formato del contexto [1]."""
    from datetime import date
    fecha = date.today().isoformat()
    entry = f"""#### MON-{fecha}-XXX: {titulo}

**Fecha**: {fecha}
**Tipo de Alerta**: {tipo_alerta}
**Disparador**: {disparador}
**Contexto**: {contexto}
**Respuesta**: {respuesta}
**Resolución**: {resolucion}
**Estado**: ABIERTO
**Responsable**: {responsable}
---
"""
    with open(ARCHIVO_REGISTRO, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"📋 Caso registrado: {titulo}")

def generar_auditoria_b6(tema, modelos, prompt_maestro):
    """Genera una plantilla de auditoría cruzada B.6 [1]."""
    from datetime import date
    fecha = date.today().isoformat()
    plantilla = f"""## Auditoría Cruzada B.6: {tema}
**Fecha**: {fecha}
**Modelos consultados**: {modelos}
**Prompt maestro**: {prompt_maestro}
"""
    return plantilla

def calcular_indice_stardust(icm, ice, ich):
    """Calcula el Índice Stardust según la tabla del contexto [1]."""
    indice = (icm + ice + ich) / 3
    nivel = ""
    if indice < 25:
        nivel = "Crítico (<25%)"
    elif indice < 50:
        nivel = "Bajo (25-50%)"
    elif indice < 75:
        nivel = "Moderado (50-75%)"
    else:
        nivel = "Excelente (>75%)"
    return {
        "ICM": icm,
        "ICE": ice,
        "ICH": ich,
        "INDICE_STARDUST": round(indice, 2),
        "NIVEL": nivel
    }

def obtener_datos_sensores(engine):
    """Simulación de lectura de sensores. Reemplaza con tu código real."""
    import random
    humedad = random.uniform(5, 95)
    temperatura = random.uniform(20, 30)
    vibracion = random.uniform(0, 0.5)
    anomalia = (humedad < 10) or (humedad > 90)
    return {
        "temperatura": round(temperatura, 2),
        "humedad": round(humedad, 2),
        "vibracion": round(vibracion, 3),
        "anomalia_humedad": anomalia,
        "score_armonia": round(random.uniform(0, 100), 2)
    }

def publicar_telemetria(client, datos):
    payload = {
        "timestamp": int(time.time()),
        "datos": datos
    }
    client.publish("stardust/ritual_3i/telemetria", json.dumps(payload))
    print(f"📡 Telemetría publicada: {payload}")

def publicar_ritual(client, nahual_info, tipo_evento):
    ahora = datetime.now()
    payload = {
        "timestamp": ahora.isoformat(),
        "evento": "Hunab_Ku",
        "tipo": tipo_evento,
        "nahual": {
            "es": nahual_info["es"][0] if isinstance(nahual_info["es"], list) else nahual_info["es"],
            "en": nahual_info["en"][0] if isinstance(nahual_info["en"], list) else nahual_info["en"],
            "zh": nahual_info["zh"][0] if isinstance(nahual_info["zh"], list) else nahual_info["zh"]
        }
    }
    client.publish("stardust/ritual_3i/evento", json.dumps(payload))
    print(f"🔔 Evento ritual publicado: {tipo_evento}")

def cargar_nahuales():
    try:
        with open(NAHUALES_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "nahuales" in data:
            nahuales_lista = data["nahuales"]
            formato_esperado = []
            for n in nahuales_lista:
                formato_esperado.append({
                    "es": n["keywords"]["es"],
                    "en": n["keywords"]["en"],
                    "zh": n["keywords"]["zh"]
                })
            return formato_esperado
        else:
            print("Error: el JSON de nahuales no tiene el formato esperado.")
            return None
    except Exception as e:
        print(f"Error cargando {NAHUALES_JSON}: {e}")
        return None

# ========================= MANEJADOR DE SEÑAL =========================
def signal_handler(sig, frame):
    print("\n🛑 Nodo detenido por el usuario.")
    client.disconnect()
    sys.exit(0)

# ========================= BUCLE PRINCIPAL =========================
if __name__ == "__main__":
    # Inicializar engine
    engine = EngineBioconexion()
    print("🌍 Engine de Bioconexión iniciado.")
    
    # Intentar conectar MQTT
    try:
        import paho.mqtt.client as mqtt
        client = mqtt.Client("NodoFaro_Merida")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        print(f"📡 Conectado al broker MQTT ({MQTT_BROKER}:{MQTT_PORT})")
    except ImportError:
        print("⚠️ paho-mqtt no instalado. Instálalo con: pip install paho-mqtt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error conectando al broker: {e}")
        sys.exit(1)
    
    # Cargar nahuales
    nahuales = cargar_nahuales()
    if nahuales:
        print(f"🦅 {len(nahuales)} nahuales cargados.")
    
    # Registrar manejador de señal
    signal.signal(signal.SIGINT, signal_handler)
    
    # Bucle principal
    try:
        while True:
            # 1. Obtener datos de sensores
            datos = obtener_datos_sensores(engine)
            
            # 2. Publicar telemetría
            publicar_telemetria(client, datos)
            
            # 3. Si hay anomalía, registrar caso
            if datos["anomalia_humedad"]:
                registrar_caso(
                    titulo=f"Anomalía de humedad: {datos['humedad']}%",
                    tipo_alerta="Roja",
                    disparador="Lectura fuera de rango (10-90%)",
                    contexto=f"Humedad registrada: {datos['humedad']}%",
                    respuesta="Notificación automática de telemetría",
                    resolucion="Pendiente de revisión",
                    responsable="Gaia Dev Assistant"
                )
                print("⚠️ Alerta de anomalía registrada.")
            
            # 4. Publicar evento ritual (primer nahual disponible como ejemplo)
            if nahuales:
                publicar_ritual(client, nahuales[0], "inicio_ciclo")
            
            # 5. Calcular y mostrar Índice Stardust simulado
            stardust = calcular_indice_stardust(
                icm=datos["score_armonia"] * 0.8,
                ice=datos["temperatura"] * 2,
                ich=datos["humedad"]
            )
            print(f"🌟 Índice Stardust: {stardust['INDICE_STARDUST']}% - {stardust['NIVEL']}")
            
            # 6. Esperar 15 minutos
            print(f"⏳ Próxima publicación en {INTERVALO_PUBLICACION//60} minutos...")
            time.sleep(INTERVALO_PUBLICACION)
    except KeyboardInterrupt:
        signal_handler(None, None)
