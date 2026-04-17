/# 🌍 Nodo Faro Mérida – Primer Nodo de la Red Stardust

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

- ## 📡 Protocolo de Telemetría Puente Cósmico
El Nodo Faro Mérida utiliza el motor `engine_bioconexion.py` para enriquecer los datos IoT con metadatos astronómicos:

- **harmony_factor**: Resonancia con el ciclo 9.9.16.0.0 (0.0 a 1.0).
- **long_count**: Fecha en Cuenta Larga (Baktun.Katun.Tun.Uinal.Kin).
- **venus_status**: Estado del ciclo de 584 días (Morning Star/Evening Star/Conjunction).
- **lunar_age**: Edad de la luna (Serie Suplementaria).


---

## 🚀 Puesta en marcha (desde cero)

### 1. Clonar el repositorio
```bash
git clone https://github.com/bioconexion3i/convocatoriapuentecosmico2027-2079.git ~/nodo_merida
cd ~/nodo_merida
