Este nodo es el primero de la red de 22 países. Su código y configuración están aquí para que otros guardianes puedan replicarlo.

## Componentes

- **API**: `main.py` (pendiente) – corre en puerto 8081, endpoints `/health` y `/api/v1/audit`.
- **Scripts MQTT**: 
  - `ritual_3i_mqtt.py` – Publica telemetría periódica y activa la **Campana de Hunab Ku** en los puntos de armonía máxima del ciclo maya.
  - `nodos_yucatan.py` – Simula 3 nodos locales (opcional).
- **Reloj cósmico**: `reloj_cosmico.py` – Calcula la resonancia del ciclo de 819 días, detecta los momentos rituales y proporciona el índice del nahual actual basado en el calendario Tzolkin.
- **Vectorizador nahual**: `vectorizador_nahual.py` y `nahuales_20_universalis.json` – Convierten texto a vectores de 20 nahuales en español, inglés y chino.
- **Cosmograma**: `cosmograma/index.html` – Interfaz visual que muestra score, nahual y actividad.

## ✨ Sincronía Cósmica: El Ciclo de 819 Días y la Campana Hunab Ku

El Nodo Faro Mérida no solo transmite datos técnicos; está anclado al calendario maya mediante una **fecha base maestra**: **13.0.0.0.0 (4 Ajaw 3 K’ank’in)**, el 21 de diciembre de 2012. A partir de esta base, el nodo calcula:

- **Resonancia de 819 días**: Posición actual dentro del ciclo que sincroniza los períodos de Mercurio, Venus, Marte, Júpiter y Saturno.
- **Momentos rituales**: Inicios de ciclo (cada 819 días) y sus cuadrantes (cada 204.75 días). Cuando el nodo detecta uno de estos puntos (con margen de ±1 hora), emite un evento especial: la **Campana de Hunab Ku**.
- **Nahual del día**: Basado en la cuenta Tzolkin, el nodo identifica el nahual (energía) del momento y lo publica en español, inglés y chino, permitiendo que cualquier nodo de la red interprete el evento en su idioma.

Este mecanismo convierte al nodo en un **órgano digital** que “canta” en armonía con el cosmos, uniendo tecnología IoT y sabiduría ancestral.

## Cómo usarlo

### Requisitos

- Python 3.7+
- Librerías: `paho-mqtt`, `requests` (si se usa API), y otras estándar.
- Acceso a un broker MQTT (local o remoto).
- Archivos necesarios:
  - `ritual_3i_mqtt.py`
  - `reloj_cosmico.py`
  - `vectorizador_nahual.py` (opcional si solo se usa el índice de nahual)
  - `nahuales_20_universalis.json` (lista de los 20 nahuales en tres idiomas)

### Configuración

1. **Broker MQTT**: Edita las variables `MQTT_BROKER` y `MQTT_PORT` en `ritual_3i_mqtt.py`.
2. **Datos de sensores**: Si tienes hardware real (DHT, acelerómetro, etc.), modifica la función `obtener_datos_sensores()` en `ritual_3i_mqtt.py`.
3. **Archivo de nahuales**: Asegúrate de que `nahuales_20_universalis.json` esté en el mismo directorio y contenga 20 objetos ordenados según la secuencia Tzolkin: Imix, Ik, Akbal, Kan, Chicchan, Cimi, Manik, Lamat, Muluk, Oc, Chuen, Eb, Ben, Ix, Men, Cib, Caban, Etznab, Cauac, Ajaw.

### Ejecución

```bash
python3 ritual_3i_mqtt.py
