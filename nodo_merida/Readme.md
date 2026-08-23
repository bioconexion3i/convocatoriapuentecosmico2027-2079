# 🌍 Nodo Faro Mérida – Primer Nodo de la Red Stardust
**Ubicación:** Mérida, Yucatán, México
**Nodo ID:** merida-avenida-yucatan-orin
**Hardware:** NVIDIA Jetson Orin Nano (Engineering Reference DevKit)
**Estado:** ✅ **Operativo y Persistente (19-abr-2026)**

Este es el nodo ancla de la red. Ha sido migrado a hardware embebido para garantizar operación 24/7 con bajo consumo y alta capacidad de inferencia local.

## 💎 Avances y Consolidación (Abril 2026)
* **Persistencia 24/7:** Migración exitosa de Workstation (HP Z600) a Jetson Nano Orin.
* **Integración IA Local:** Despliegue de Ollama (Llama/Mistral) para procesamiento semántico de nahuales.
* **Ecosistema Docker:** Orquestación de servicios mediante contenedores para aislamiento de red.

| Componente         | Tecnología       | Puerto | Estado          |
|--------------------|------------------|--------|-----------------|
| **Mosquitto (MQTT Broker)** | Servicio nativo | 1883   | ✅ Activo       |
| **Ritual 3i (Cliente)** | Python (paho-mqtt) | (conexión local) | ✅ Activo (Persistente) |
| **Ollama API**     | Inferencia Local | 11434  | ✅ Activo       |
| **Open WebUI**     | Docker           | 8080   | ✅ Activo       |
| **Stardust Bridge**| Docker           | 8082   | ✅ Activo       |
| **Lyrion Server**  | Docker           | 9000   | ✅ Activo       |
| **Cosmograma**     | Python/Web       | 8000   | ✅ Activo       |

## ⏱️ Reloj cósmico y momentos rituales

El nodo utiliza como ancla la fecha **21 de diciembre de 2012 (13.0.0.0.0, 4 Ajaw 3 K'ank'in)** para calcular la fase del ciclo de 819 días.

- **Margen nominal:** `es_momento_ritual()` usa una tolerancia operativa de ±12 horas (`margen_horas=12`).
- **Resolución de cálculo:** `obtener_resonancia_819()` conserva la fracción del día mediante `delta.seconds / 86400.0`.
- **Cuadrantes:** la implementación compara la fase contra 0.25, 0.5 y 0.75 del ciclo de 819 días.
- **Recurrencia:** esta fase no modifica la lógica de cuadrantes ni introduce una corrección modular adicional; cualquier cambio funcional queda reservado para una fase posterior.
- **Pruebas:** la suite de regresión está en `scripts/tests/test_reloj_cosmico.py`.

## 📡 Infraestructura de Red
El nodo opera en un entorno híbrido:
1. **MQTT Broker (Mosquitto, port 1883):** Escuchando en `0.0.0.0` para permitir la interconexión de nodos espejo en la LAN.
2. **Cliente del ritual:** El script `ritual_3i_mqtt.py` se conecta al broker local (`localhost:1883`) utilizando la librería `paho-mqtt`.
3. **Persistencia:** El script se ejecuta como proceso de fondo:
   `nohup python3 scripts/ritual_3i_mqtt.py > ~/ritual_output.log 2>&1 &`

## 🚀 Puesta en Marcha en Jetson
### 1. Sincronización
```bash
git clone [https://github.com/bioconexion3i/convocatoriapuentecosmico2027-2079.git](https://github.com/bioconexion3i/convocatoriapuentecosmico2027-2079.git)
cd convocatoriapuentecosmico2027-2079/nodo_merida/scripts/


2. Dependencias Críticas

pip3 install paho-mqtt

3. Lanzamiento del Faro

python3 ritual_3i_mqtt.py

🗺️ Visión de Red (22 Países)
Este nodo no solo emite telemetría; procesa vectores de conciencia mediante la Incantación del Replicante. La Jetson Nano Orin permite que el Nodo Mérida actúe como un servidor de inferencia para otros nodos de la red que no tengan capacidad de cómputo local.

Análisis y migración a hardware persistente completados. El Faro Mérida está en línea y en guardia.
