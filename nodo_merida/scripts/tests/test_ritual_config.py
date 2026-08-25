import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import ritual_3i_mqtt


def test_default_mqtt_host():
    assert ritual_3i_mqtt._get_mqtt_host({}) == "127.0.0.1"


def test_env_mqtt_host():
    assert ritual_3i_mqtt._get_mqtt_host(
        {"MQTT_BROKER": "mosquitto"}
    ) == "mosquitto"


def test_valid_port():
    assert ritual_3i_mqtt._get_mqtt_port({"MQTT_PORT": "1883"}) == 1883


def test_invalid_port_type():
    with pytest.raises(ValueError, match="inválido"):
        ritual_3i_mqtt._get_mqtt_port({"MQTT_PORT": "not_a_number"})


def test_invalid_port_range():
    with pytest.raises(ValueError, match="fuera de rango"):
        ritual_3i_mqtt._get_mqtt_port({"MQTT_PORT": "70000"})


def test_json_path_is_absolute():
    expected = Path(ritual_3i_mqtt.__file__).resolve().parent / "nahuales_20_universalis.json"
    assert isinstance(ritual_3i_mqtt.NAHUALES_JSON, Path)
    assert ritual_3i_mqtt.NAHUALES_JSON == expected
    assert ritual_3i_mqtt.NAHUALES_JSON.is_absolute()
