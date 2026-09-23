# Nodo Faro Mérida

Nodo publicador de telemetría de la red Stardust.

- Ubicación: Mérida, Yucatán, México.
- Nodo: `merida-avenida-yucatan-orin`.
- Hardware validado: NVIDIA Jetson Orin Nano.
- Servicio principal: `faro_publisher`.
- Estado: operativo mediante Docker Compose.

## Arquitectura

El publicador corre dentro de un contenedor Docker y utiliza el broker Mosquitto nativo de la Jetson.

```text
faro_publisher
    │
    └── host.docker.internal:1884
              │
              └── Mosquitto nativo en la Jetson
```

El broker no se ejecuta dentro de este Compose. Esto evita duplicar el servicio Mosquitto y mantiene un único broker para el host y los nodos locales.

Además del publicador, el nodo tiene otros tres servicios contenedorizados:

- `oraculo-del-dia` — genera el oráculo diario a las 06:00 America/Merida y lo publica en `stardust/merida/evento`.
- `stardust_bridge` — puente HTTP que expone oráculo y telemetría bajo un solo host.
- `open-webui` — interfaz de chat que consume el bridge como Tool.

## Modo operativo

El modo operativo oficial del Nodo Faro Mérida es Docker Compose mediante el
servicio `faro_publisher`.

El servicio systemd histórico `ritual-stardust.service` ejecutaba el mismo
publicador directamente en el host. Fue deshabilitado para evitar dos
instancias publicando simultáneamente en
`stardust/merida/telemetria`.

No deben ejecutarse ambos modos a la vez, porque producirían telemetría
duplicada y dificultarían el diagnóstico.

Comprobar el modo activo:

```bash
docker compose -f nodo_merida/docker-compose.yml ps
docker compose -f nodo_merida/docker-compose.yml logs -f faro_publisher
systemctl is-active ritual-stardust.service
```

El estado esperado del servicio histórico es:

```text
inactive
```

El servicio systemd se conserva deshabilitado como mecanismo de rollback
temporal. Si fuera necesario utilizarlo, primero debe detenerse Docker:

```bash
docker compose -f nodo_merida/docker-compose.yml down
sudo systemctl enable --now ritual-stardust.service
```

Para volver al modo Docker:

```bash
sudo systemctl disable --now ritual-stardust.service
docker compose -f nodo_merida/docker-compose.yml up -d
```

## Broker MQTT

### Listener del host

La configuración validada en la Jetson es:

| Listener | Uso |
|---|---|
| `127.0.0.1:1883` | Clientes locales del host |
| `172.17.0.1:1884` | Clientes desde la red bridge de Docker |

Desde el contenedor se utiliza:

```text
host.docker.internal:1884
```

El Compose agrega:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

El listener de Docker está restringido a la interfaz `172.17.0.1`.

### Seguridad actual (endurecida 2026-08-24)

El broker exige autenticación en todos los listeners:

```text
allow_anonymous false
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/acl.conf
listener 1884 172.17.0.1
```

Configuración ubicada en `/etc/mosquitto/conf.d/nodo-faro.conf`.

El publicador se autentica con `username_pw_set()` usando `MQTT_USER`/`MQTT_PASSWORD`
desde el entorno (`.env`, ignorado por Git). Nunca guardar contraseñas, tokens ni
archivos de credenciales en el repositorio.

Los listeners están ligados a `127.0.0.1` y `172.17.0.1`. Antes de exponer el nodo
fuera de este entorno: firewall y revisión periódica de la ACL.

### Roles MQTT

La ACL separa publicación y lectura:

| Usuario | Permiso | Uso |
|---|---|---|
| `merida_pub` | `write stardust/merida/#` | `faro_publisher`, `oraculo-del-dia` |
| `exar_lector` | `read stardust/#` | `stardust_bridge`, herramientas de lectura |

Las credenciales viven en `.env` (publicador) y `.env.lector` (lector),
ambos ignorados por Git. Rotar la contraseña de `exar_lector` periódicamente.

## Tópico

El publicador envía telemetría a:

```text
stardust/merida/telemetria
```

El payload incluye:

- timestamp UTC;
- identificador del nodo;
- latido;
- estado de `engine_bioconexion`;
- nahual del día.

El servicio `oraculo-del-dia` publica además en:

```text
stardust/merida/evento
```

con el JSON del oráculo diario (`tipo: oraculo_diario`).

## Dependencias

Las dependencias están fijadas en:

```text
nodo_merida/requirements.txt
```

Versión validada:

```text
paho-mqtt==2.1.0
```

El cliente utiliza:

```python
mqtt.CallbackAPIVersion.VERSION2
```

## Ejecución con Docker Compose

Desde la raíz del repositorio:

```bash
docker compose -f nodo_merida/docker-compose.yml build --no-cache
docker compose -f nodo_merida/docker-compose.yml up -d
```

Comprobar el estado:

```bash
docker compose -f nodo_merida/docker-compose.yml ps
docker compose -f nodo_merida/docker-compose.yml logs -f faro_publisher
```

Detener el nodo:

```bash
docker compose -f nodo_merida/docker-compose.yml down
```

## Observación de telemetría

Desde la Jetson:

```bash
mosquitto_sub \
  -h 172.17.0.1 \
  -p 1884 \
  -u "$MQTT_USER" -P "$MQTT_PASSWORD" \
  -t 'stardust/merida/#' \
  -v
```

Una publicación correcta aparece en:

```text
stardust/merida/telemetria
```

Y el evento diario del oráculo en:

```text
stardust/merida/evento
```

## Validación

Ejecutar la suite:

```bash
pytest -q
```

Validar sintaxis:

```bash
python3 -m py_compile nodo_merida/scripts/ritual_3i_mqtt.py
```

Validar Compose:

```bash
docker compose -f nodo_merida/docker-compose.yml config
```

Comprobar imports dentro del contenedor:

```bash
docker compose -f nodo_merida/docker-compose.yml run --rm faro_publisher \
  python -c "import ritual_3i_mqtt, engine_bioconexion; print('IMPORTS OK')"
```

La validación operacional realizada confirmó:

- 43 pruebas exitosas;
- build Docker sin caché;
- conexión a `host.docker.internal:1884`;
- carga de 20 nahuales;
- publicación en `stardust/merida/telemetria`;
- recuperación después de reiniciar Mosquitto;
- cierre limpio ante detención del contenedor.

## Reconexión

El publicador reutiliza el mismo cliente MQTT y aplica reintentos con espera progresiva cuando detecta que el broker no está conectado.

La recuperación del proceso fue validada operacionalmente. Sin embargo, las publicaciones generadas durante una caída no tienen todavía una cola persistente. Por eso QoS 1 no debe interpretarse como garantía de entrega de eventos creados mientras el broker está fuera de servicio.

La persistencia de Mosquitto está habilitada en el host, pero esto no crea
una cola persistente para las publicaciones que el proceso Python genere
mientras el broker está desconectado. Las publicaciones emitidas durante esa
caída pueden perderse, especialmente si el proceso o el contenedor se reinicia
antes de reconectar.

## Puente HTTP — Stardust Bridge (2026-09-23)

El nodo expone un puente HTTP que unifica oráculo y telemetría bajo un solo
host, para que interfaces como Open WebUI puedan consultarlos sin conocer
MQTT ni las rutas internas del broker.

### Servicio

Corre en `stardust_bridge/` como contenedor Docker independiente.

| Endpoint | Devuelve |
|---|---|
| `GET /health` | Estado del bridge (MQTT conectado, último mensaje) |
| `GET /oraculo/hoy` | JSON del oráculo del día (leído del archivo local) |
| `GET /oraculo/{fecha}` | JSON del oráculo de una fecha (`YYYY-MM-DD`) |
| `GET /telemetria/latest` | Último payload MQTT de `stardust/merida/telemetria` |
| `POST /api/chat` | Proxy a Ollama (`host.docker.internal:11434`) |

Escucha en `0.0.0.0:8082` para ser alcanzable desde otros contenedores
(Open WebUI, futuros Workers). No debe exponerse fuera de la LAN sin
autenticación adicional.

### Diagrama del estado actual

```text
faro_publisher (ritual_3i_mqtt.py)
        │
        ├──> Mosquitto host :1884
        │       ├── stardust/merida/telemetria (cada 30s)
        │       └── stardust/merida/evento     (diario 06:00)
        │
oraculo-del-dia (oraculo_del_dia.py)
        │
        └──> Mosquitto host :1884 → stardust/merida/evento
                │
                └──> archivos en oraculo_dia/salida/YYYY-MM-DD.json

stardust_bridge
        ├── MQTT (exar_lector) → último payload de telemetría
        ├── lectura directa     → oraculo_dia/salida/*.json
        └── HTTP :8082          → Open WebUI / Workers / cualquier cliente
```

### Corrección del oráculo (2026-09-23)

El servicio `oraculo-del-dia` llevaba desde su despliegue sin publicar en
MQTT: su `docker-compose.yml` declaraba `env_file: .env`, pero el archivo
vive en el directorio padre. Corregido a `env_file: ../.env`. Desde entonces
publica correctamente en `stardust/merida/evento`.

Los archivos JSON diarios nunca se perdieron — siempre se generaron en
`oraculo_dia/salida/`. El endpoint `/oraculo/{fecha}` los expone para
recuperar cualquier día del historial.

### Tool de Open WebUI — Maya Oracle Faro Mérida v2.0

En `Workspace → Tools` de Open WebUI. Consulta el bridge extendido y expone
tres funciones al modelo:

- `get_maya_oracle()` → oráculo del día.
- `get_faro_telemetry()` → latido, Venus, nahual del día.
- `get_mantra_if_first_time_today()` → mantra solo la primera vez del día
  (persistido en `/app/backend/data/maya_oracle_last_date.txt`).

Verificado en chat: el modelo cruza telemetría y oráculo y produce una
síntesis coherente del día. Ejemplo validado el 2026-09-23 con `gemma4:cloud`.

### Verificación rápida

```bash
curl -s http://127.0.0.1:8082/health | jq
curl -s http://127.0.0.1:8082/oraculo/hoy | jq '.kin, .don'
curl -s http://127.0.0.1:8082/telemetria/latest | jq '.recibido, .payload.latido'
```

### Rotación de credenciales

```bash
sudo mosquitto_passwd /etc/mosquitto/passwd exar_lector
sudo systemctl reload mosquitto
nano .env.lector
docker compose -f stardust_bridge/docker-compose.yml up -d --force-recreate
```

## Archivos principales

- `Dockerfile`: imagen del publicador.
- `docker-compose.yml`: conexión al broker nativo.
- `requirements.txt`: dependencias fijadas.
- `scripts/ritual_3i_mqtt.py`: publicador MQTT.
- `scripts/engine_bioconexion.py`: motor de estado.
- `scripts/nahuales_20_universalis.json`: archivo canónico usado por el publicador.
- `scripts/tests/`: pruebas automatizadas.
- `oraculo_dia/`: servicio contenedorizado que genera el oráculo diario en `salida/`.
- `stardust_bridge/`: puente HTTP que unifica oráculo y telemetría (FastAPI + MQTT).
- `scripts/oraculo_del_dia.py`: generador del oráculo diario.
- `scripts/logger_mqtt.py`: logger MQTT a CSV (usado para análisis externo).
- `scripts/vectorizador_pipeline.py`: vectorización de textos hacia 20D nahual.
- `scripts/verify_oracle_delivery.py`: validación de entrega del oráculo por MQTT.

## Seguimientos

- añadir una cola persistente si se requiere entrega durante caídas;
- mejorar los logs explícitos de desconexión y reconexión;
- automatizar una prueba de integración Docker/MQTT;
- evaluar un Last Will para el estado del nodo;
- evaluar la exposición del bridge fuera de la LAN (Cloudflare Tunnel o similar)
  con autenticación previa;
- considerar un backfill del historial 09-09 al 22-09 si se requiere
  completar el canal MQTT (los archivos en `oraculo_dia/salida/` están a salvo);
- mantener este README sincronizado con la configuración real de la Jetson.
