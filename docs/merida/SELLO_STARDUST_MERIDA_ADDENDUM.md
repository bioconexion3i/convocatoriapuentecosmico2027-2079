# Anexo del Sello Stardust — Nodo Faro Mérida

**Fecha de actualización:** 2026-08-24  
**Nodo:** `merida-avenida-yucatan-orin`  
**Hardware:** NVIDIA Jetson Orin Nano  
**Documento base:** `SELLO_STARDUST_EXPANDIDO.md`

## Propósito

Este anexo registra la operación efectiva del Nodo Faro Mérida después de la
migración desde el publicador systemd hacia Docker Compose. Su objetivo es
mantener el Sello sincronizado con el estado verificable del nodo sin
presentar como completadas capacidades que todavía son trabajo pendiente.

## Modo operativo oficial

El modo oficial de publicación es Docker Compose mediante:

```text
faro_publisher
```

El servicio histórico:

```text
ritual-stardust.service
```

queda deshabilitado para evitar dos instancias publicando simultáneamente.
No deben ejecutarse ambos modos a la vez porque producirían telemetría
duplicada y dificultarían el diagnóstico.

## Topología MQTT

Mosquitto continúa ejecutándose como servicio nativo en la Jetson.

| Listener | Uso |
|---|---|
| `127.0.0.1:1883` | Clientes locales del host |
| `172.17.0.1:1884` | Publicador dentro de Docker |

El contenedor utiliza:

```text
host.docker.internal:1884
```

`host.docker.internal` se resuelve mediante `extra_hosts` a la pasarela Docker,
actualmente `172.17.0.1`.

Los listeners no están ligados a todas las interfaces de red. Aun así, el
broker permite conexiones anónimas dentro de los ámbitos configurados.

## Estado de seguridad

La configuración actual debe considerarse operativa y local, no una postura
final de producción.

Pendientes:

- usuario MQTT dedicado;
- credenciales fuera del repositorio;
- ACL limitada por tópico;
- validación de permisos de publicación y suscripción;
- revisión de reglas de firewall antes de cualquier exposición adicional.

No deben guardarse contraseñas, tokens ni archivos de credenciales en Git.

## Garantías de entrega

La persistencia de Mosquitto está habilitada en el host, pero no existe todavía
una cola persistente para publicaciones que el proceso Python genere mientras
el broker está desconectado.

QoS 1 cubre mensajes en vuelo con conexión activa. No garantiza la entrega de
eventos creados durante una caída del broker. Esos eventos pueden perderse si
el proceso o el contenedor se reinicia antes de recuperar la conexión.

## Fuente de datos de nahuales

El publicador carga:

```text
nodo_merida/scripts/nahuales.json
```

Ese archivo contiene 20 entradas y es la fuente canónica del publicador.

El archivo:

```text
nodo_merida/scripts/nahuales_20_universalis.json
```

es alternativo, contiene también 20 entradas y no es utilizado actualmente por
`ritual_3i_mqtt.py`. Su mantenimiento queda pendiente de una decisión
separada.

## Relación con el Sello base

Este anexo prevalece para el estado operativo específico del Nodo Faro Mérida
cuando exista una diferencia entre la descripción histórica del documento base
y la configuración validada del nodo.

Cualquier cambio futuro de autenticación, ACL, persistencia, transporte,
supervisor de procesos o contrato de tópicos debe actualizar este anexo y el
README operativo del nodo.

## Validación registrada

La migración fue validada con:

- Docker Compose operativo;
- un único publicador activo;
- `ritual-stardust.service` inactivo y deshabilitado;
- publicación en `stardust/merida/telemetria`;
- identificador `merida-avenida-yucatan-orin`;
- recuperación del publicador después de reiniciar Mosquitto;
- checks automatizados de GitHub exitosos en la PR de documentación.
