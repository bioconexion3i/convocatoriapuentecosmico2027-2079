# 🌍 Nodo Faro Mérida – Primer Nodo de la Red Stardust

**Ubicación:** Mérida, Yucatán, México  
**Nodo ID:** `merida-avenida-yucatan`  
**Score actual:** Variable (se consulta vía API)  
**Ritmo:** Publica cada 30-60 segundos vía MQTT  
**Estado:** ✅ Operativo (08-abr-2026)

Este nodo es el primero de la red de 22 países. Su código y configuración están aquí para que otros guardianes puedan replicarlo.

---

## 📂 Componentes y servicios

| Componente | Tecnología | Puerto | Estado |
|------------|------------|--------|--------|
| API Stardust | FastAPI (Docker) | `8082` | ✅ Activo |
| Broker MQTT (TCP) | Mosquitto | `1883` | ✅ Activo |
| Broker MQTT (WebSocket) | Mosquitto | `9001` | ✅ Activo |
| Cosmograma (web) | HTML/JS + Python http.server | `8000` | ✅ Activo |
| Scripts productores | Python (paho-mqtt) | - | ✅ Activos |

### Scripts incluidos
- `ritual_3i_mqtt.py` – Publica eventos del ritual 3i (cenit, nahual del día).
- `nodos_yucatan.py` – Simula 3 nodos locales publicando scores y métricas.
- `reloj_cosmico.py` – Calcula ciclos mayas y momentos rituales.
- `vectorizador_nahual.py` – Convierte texto a vectores de nahuales.
- `nahuales_20_universalis.json` – Base de datos de los 20 nahuales.

### Interfaz visual
- `cosmograma/index.html` – Muestra score en tiempo real, nahual actual, fase lunar y eventos MQTT.

---

## 🚀 Puesta en marcha (desde cero)

### 1. Clonar el repositorio
```bash
git clone https://github.com/bioconexion3i/convocatoriapuentecosmico2027-2079.git ~/nodo_merida
cd ~/nodo_merida
