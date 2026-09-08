# Oraculo del Dia - Nodo Faro Merida

Servicio contenerizado que genera una vez al dia (06:00, America/Merida)
el estado cosmico extendido del nodo (Sak Tahn Waax + Kin completo)
con interpretacion oracular, y lo publica en el broker MQTT.

## Despliegue

```bash
docker compose -f nodo_merida/oraculo_dia/docker-compose.yml build --no-cache
docker compose -f nodo_merida/oraculo_dia/docker-compose.yml up -d
docker compose -f nodo_merida/oraculo_dia/docker-compose.yml logs -f oraculo
```

Credenciales: crear `nodo_merida/oraculo_dia/.env` con MQTT_USER y MQTT_PASSWORD
(mismo usuario de Mosquitto que faro_publisher). Archivo en .gitignore.

## ACL de Mosquitto (host)

El broker exige autenticacion y ACL. El usuario del oraculo necesita permiso
de escritura en `stardust/merida/evento`. Si se reutiliza el usuario de
faro_publisher, verificar que su ACL lo cubra; si no, agregar entrada en
/etc/mosquitto/acl.conf y reiniciar Mosquitto.

## Validacion local (sin Docker)

```bash
cd nodo_merida/scripts
python3 tests/test_engine.py        # 9 pruebas
python3 oraculo_del_dia.py --hoy    # imprime y guarda en salida/
```

## Relacion con faro_publisher

Publica una vez al dia en `stardust/merida/evento` — no interfiere con la
telemetria de `stardust/merida/telemetria` (cada 30 s). Servicios independientes.
