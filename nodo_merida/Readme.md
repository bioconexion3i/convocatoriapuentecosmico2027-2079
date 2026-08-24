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

### Seguridad actual

La configuración actual del listener permite conexiones anónimas dentro del entorno Docker local:

```text
allow_anonymous true
```

Esto debe considerarse una configuración operativa local, no una postura final de producción. El endurecimiento pendiente incluye:

- usuario MQTT dedicado;
- credenciales fuera del repositorio;
- ACL limitada por tópico;
- validación de permisos de publicación y suscripción.

Nunca deben guardarse contraseñas, tokens ni archivos de credenciales en Git.

Los listeners están ligados a `127.0.0.1` y `172.17.0.1`, no a todas las
interfaces de red. Aun así, permiten conexiones anónimas desde los procesos
locales y la red bridge de Docker. Antes de exponer el nodo fuera de este
entorno deben configurarse autenticación, ACL y firewall.

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
  -t 'stardust/merida/#' \
  -v
```

Una publicación correcta aparece en:

```text
stardust/merida/telemetria
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

## Archivos principales

- `Dockerfile`: imagen del publicador.
- `docker-compose.yml`: conexión al broker nativo.
- `requirements.txt`: dependencias fijadas.
- `scripts/ritual_3i_mqtt.py`: publicador MQTT.
- `scripts/engine_bioconexion.py`: motor de estado.
- `scripts/nahuales.json`: archivo canónico usado por el publicador.
- `scripts/tests/`: pruebas automatizadas.

## Seguimientos

- sustituir acceso anónimo por autenticación y ACL;
- añadir una cola persistente si se requiere entrega durante caídas;
- mejorar los logs explícitos de desconexión y reconexión;
- automatizar una prueba de integración Docker/MQTT;
- evaluar un Last Will para el estado del nodo;
- mantener este README sincronizado con la configuración real de la Jetson.
