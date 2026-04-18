# 🌍 Nodo Faro Mérida – Primer Nodo de la Red Stardust
**Ubicación:** Mérida, Yucatán, México
**Nodo ID:** merida-avenida-yucatan
**Score actual:** Sincronizado vía harmony_factor
**Ritmo:** Publica cada 30-60 segundos vía MQTT
**Estado:** ✅ **Operativo y Validado (17-abr-2026)**
Este nodo es el primero de la red de 22 países. Su código y configuración están aquí para que otros guardianes puedan replicarlo e integrarse al **Puente Cósmico 2027-2079**.
## 💎 Avances y Consolidación (Abril 2026)
 * **Integración Total:** Vinculación del script productor con el motor engine_bioconexion.py.
 * **Sincronía Galáctica:** Implementación del **Supernúmero 9.9.16.0.0** para el cálculo del harmony_factor universal.
 * **Interoperabilidad IA:** Payload optimizado con vectores normalizados para procesamiento por modelos de lenguaje.
## 📂 Componentes y Servicios
| Componente | Tecnología | Puerto | Estado |
|---|---|---|---|
| API Stardust | FastAPI (Docker) | 8082 | ✅ Activo |
| Broker MQTT (TCP) | Mosquitto | 1883 | ✅ Activo |
| Broker MQTT (WS) | Mosquitto | 9001 | ✅ Activo |
| Cosmograma (Web) | HTML/JS + Python | 8000 | ✅ Activo |
| Scripts Productores | Python (paho-mqtt) | - | ✅ Activos |
### Scripts Incluidos
 * **ritual_3i_mqtt.py**: Integrador principal. Publica el payload unificado (IoT + Astronomía).
 * **engine_bioconexion.py**: Motor matemático basado en los cálculos arqueoastronómicos de Anthony F. Aveni.
 * **nodos_yucatan.py**: Simulador de red local (3 nodos secundarios) para pruebas de carga y métricas.
 * **reloj_cosmico.py**: Gestión de la cuenta larga, fases lunares y momentos rituales cenitales.
 * **vectorizador_nahual.py**: Herramienta de NLP que convierte texto a vectores basados en los 20 nahuales.
 * **nahuales_20_universalis.json**: Base de datos semántica y descriptiva de los nahuales.
### Interfaz Visual
 * **cosmograma/index.html**: Dashboard en tiempo real que visualiza el score de armonía, el nahual del día y el tráfico de eventos MQTT.
## 📡 Protocolo de Telemetría Puente Cósmico
El Nodo Faro Mérida utiliza el motor de bioconexión para enriquecer los datos de sensores físicos con metadatos astronómicos:
 * **harmony_factor**: Resonancia normalizada con el ciclo 9.9.16.0.0 (0.0 a 1.0).
 * **long_count**: Fecha exacta en Cuenta Larga (Baktun.Katun.Tun.Uinal.Kin).
 * **venus_status**: Estado del ciclo sinódico (Morning Star / Evening Star / Conjunction).
 * **lunar_series**: Edad de la luna y fase (Serie Suplementaria).
 * **kawiil_819**: Fase y cuadrante (color/dirección) del ciclo de 819 días.
## 🚀 Puesta en Marcha (Desde Cero)
### 1. Clonar el Repositorio
```bash
git clone https://github.com/bioconexion3i/convocatoriapuentecosmico2027-2079.git ~/nodo_merida
cd ~/nodo_merida/nodo_merida

```
### 2. Instalación de Dependencias
```bash
pip install -r requirements.txt

```
### 3. Ejecución del Faro
Para iniciar la publicación de datos del Nodo Mérida:
```bash
python3 scripts/ritual_3i_mqtt.py

```
## 🗺️ Visión de Red (22 Países)
Este repositorio contiene la **Incantación del Replicante**, permitiendo que otros 21 guardianes activen nodos espejo. La estandarización matemática asegura que toda la red lata bajo la misma pulsación galáctica, transformando datos locales en conciencia global.
*Análisis y consolidación técnica completados. El Faro Mérida está en línea.*
