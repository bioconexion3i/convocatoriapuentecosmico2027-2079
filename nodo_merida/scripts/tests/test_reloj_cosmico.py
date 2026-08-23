"""
Pruebas unitarias del reloj cósmico del Nodo Faro Mérida.

Alcance:
  - FECHA_BASE_MAYA = 2012-12-21 (13.0.0.0.0, 4 Ajaw 3 K'ank'in),
    conforme a nodo_merida/Readme.md (fuente normativa).
  - Inicios de ciclo cada 819 días.
  - Cuadrantes cada 204.75 días con margen de ±0.5 días (±12 h).
  - es_momento_ritual() en fronteras, vísperas y fechas reales.
  - Cobertura total de esta versión: 37 casos.

Restricciones respetadas:
  - La firma de es_momento_ritual() NO se modifica; la fecha se controla
    sustituyendo `datetime` en el namespace del módulo (monkeypatch).
  - No se extraen constantes del módulo: las pruebas usan literales.
  - Sin red, sin MQTT, sin servicios: importar reloj_cosmico no publica nada.

Ejecución:
    python -m pytest nodo_merida/scripts/tests/test_reloj_cosmico.py -v
"""

import os
import sys
from datetime import datetime, timedelta

import pytest

# Permite ejecutar pytest desde cualquier directorio del repositorio
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import reloj_cosmico  # noqa: E402

BASE = datetime(2012, 12, 21)  # 13.0.0.0.0 — nodo_merida/Readme.md


@pytest.fixture
def con_fecha(monkeypatch):
    """Fija datetime.now() visto por reloj_cosmico a una fecha arbitraria.

    Sustituye el nombre `datetime` DENTRO del módulo por una subclase
    cuyo now() devuelve la fecha indicada. La firma pública de
    es_momento_ritual() permanece intacta. La resta entre instancias de
    la subclase y FECHA_BASE_MAYA (creada con el datetime original en el
    import) es válida por herencia: ambas son datetime.
    """

    class _RelojFijo(datetime):
        _fija = None

        @classmethod
        def now(cls, tz=None):
            return cls._fija

    def _poner(fecha):
        _RelojFijo._fija = fecha
        monkeypatch.setattr(reloj_cosmico, "datetime", _RelojFijo)

    return _poner


def _dia(n):
    """Fecha civil N días después de la fecha base maestra."""
    return BASE + timedelta(days=n)


# ---------------------------------------------------------------------------
# 1. Fecha base (regresión de la Fase A)
# ---------------------------------------------------------------------------

def test_fecha_base_maestra_es_2012():
    assert reloj_cosmico.FECHA_BASE_MAYA == BASE


def test_fecha_base_no_es_la_erronea_2020():
    # Regresión explícita (Fase A): la constante previa e incorrecta
    # era datetime(2020, 12, 21).
    assert reloj_cosmico.FECHA_BASE_MAYA.year != 2020


# ---------------------------------------------------------------------------
# 2. Inicios de ciclo (dias_desde_base % 819 == 0)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("n", [0, 819, 1638, 2457, 3276, 4095, 4914, 5733])
def test_inicio_de_ciclo_es_ritual(con_fecha, n):
    con_fecha(_dia(n))
    assert reloj_cosmico.es_momento_ritual() is True


@pytest.mark.parametrize("n", [818, 1637, 2456, 4913])
def test_dia_antes_de_inicio_no_dispara(con_fecha, n):
    con_fecha(_dia(n))
    assert reloj_cosmico.es_momento_ritual() is False


# ---------------------------------------------------------------------------
# 3. Límites de cuadrantes (fronteras fraccionarias)
#
# Tabla de verdad verificada numéricamente (2026-08-23):
#   k=1 (204.75): dispara SOLO el día 205    -> |205 - 204.75| = 0.25
#   k=2 (409.50): dispara los días 409 y 410 -> ambos a distancia 0.50
#   k=3 (614.25): dispara SOLO el día 614    -> |614 - 614.25| = 0.25
#
# Nota: aquí se prueba una SELECCIÓN de puntos vecinos alrededor de cada
# frontera, no el vecindario completo ±1/±2/±3. La asimetría de disparo
# es estructural: diffs enteros contra fronteras fraccionarias.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("n", [205, 409, 410, 614])
def test_cuadrante_dispara(con_fecha, n):
    con_fecha(_dia(n))
    assert reloj_cosmico.es_momento_ritual() is True


@pytest.mark.parametrize(
    "n", [203, 204, 206, 407, 408, 411, 412, 612, 613, 615, 616]
)
def test_vecinos_de_cuadrante_no_disparan(con_fecha, n):
    con_fecha(_dia(n))
    assert reloj_cosmico.es_momento_ritual() is False


# ---------------------------------------------------------------------------
# 4. es_momento_ritual() en días ordinarios
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("n", [79, 100, 300])
def test_dia_ordinario_no_es_ritual(con_fecha, n):
    con_fecha(_dia(n))
    assert reloj_cosmico.es_momento_ritual() is False


# ---------------------------------------------------------------------------
# 5. Fechas reales documentadas (auditadas el 2026-08-23)
# ---------------------------------------------------------------------------

def test_2026_06_05_es_inicio_de_ciclo_real(con_fecha):
    con_fecha(datetime(2026, 6, 5))  # día 4914 = 6 × 819
    assert reloj_cosmico.es_momento_ritual() is True


def test_2028_09_01_es_inicio_de_ciclo_real(con_fecha):
    con_fecha(datetime(2028, 9, 1))  # día 5733 = 7 × 819
    assert reloj_cosmico.es_momento_ritual() is True


def test_2027_07_19_y_20_son_cuadrante_k2_real(con_fecha):
    con_fecha(datetime(2027, 7, 19))  # día 409 del ciclo vigente
    assert reloj_cosmico.es_momento_ritual() is True
    con_fecha(datetime(2027, 7, 20))  # día 410 del ciclo vigente
    assert reloj_cosmico.es_momento_ritual() is True


def test_2027_07_18_y_21_no_son_rituales(con_fecha):
    con_fecha(datetime(2027, 7, 18))
    assert reloj_cosmico.es_momento_ritual() is False
    con_fecha(datetime(2027, 7, 21))
    assert reloj_cosmico.es_momento_ritual() is False


def test_hoy_de_auditoria_2026_08_23_ordinario(con_fecha):
    con_fecha(datetime(2026, 8, 23))  # día 79 del ciclo vigente
    assert reloj_cosmico.es_momento_ritual() is False
