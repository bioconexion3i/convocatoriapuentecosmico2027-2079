# 🌍 Nodo Faro Mérida – Primer Nodo de la Red Stardust

**Ubicación:** Mérida, Yucatán, México  
**Nodo ID:** `merida-avenida-yucatan`  
**Score actual:** 0.626  
**Ritmo:** Publica cada 30 segundos vía MQTT

Este nodo es el primero de la red de 22 países. Su código y configuración están aquí para que otros guardianes puedan replicarlo.

## Componentes

- **API**: `main.py` (pendiente) – corre en puerto 8081, endpoints `/health` y `/api/v1/audit`.
- **Scripts MQTT**: `ritual_3i_mqtt.py` (publica Hunab Ku y cenit) y `nodos_yucatan.py` (simula 3 nodos locales).
- **Vectorizador nahual**: `vectorizador_nahual.py` y `nahuales_20_universalis.json` – convierten texto a vectores de 20 nahuales en español, inglés y chino.
- **Cosmograma**: `cosmograma/index.html` – interfaz visual que muestra score, nahual y actividad.

## Cómo usarlo

(Instrucciones básicas...)

## Verificación en vivo

- API: `http://192.168.100.34:8081/health`
- Cosmograma: `http://192.168.100.34:8000`
- MQTT: suscribirse a `stardust/#` con `mosquitto_sub`
