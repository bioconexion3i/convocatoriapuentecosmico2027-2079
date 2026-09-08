#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
engine_bioconexion.py - Motor de estado cósmico del Nodo Faro Mérida
====================================================================
Proyecto Hunab Ku B.6 / Red Stardust / BioConexion3i

ACTUALIZACIÓN ADITIVA (2026-09-08, rama feat/bioconexion-engine-gmt):
  * SIN CAMBIOS en get_jdn, _calc_sak_tahn_waax ni get_bioconexion_state
    (ritual_3i_mqtt.py los consume con firma y forma plana actuales).
  * AGREGA fecha_a_kin_completo() y get_estado_cosmico(): Kin completo
    (Tzolk'in tono+nahual, Haab', Cuenta Larga) anclado a la correlación
    GMT: 2012-12-21 = 4 Ajaw 3 K'ank'in = 13.0.0.0.0.

Validación cruzada: la fórmula de ritual_3i_mqtt.py
    nahuales[(jdn - 584283 + 19) % 20]
es algebraicamente idéntica a la de fecha_a_kin_completo()
    (19 + delta) % 20, delta = fecha - 2012-12-21
porque 1872000 % 20 == 0. Ver tests/test_engine.py.

Anclas validadas (tests/test_engine.py):
  2012-12-21 = 4 Ajaw 3 K'ank'in 13.0.0.0.0
  2026-09-04 = 4 Chicchán 18 Mol 13.0.13.16.5 (latido 77 del nodo)
  2003-09-04 = 1 K'an 12 Mol 12.19.10.10.4
"""

import datetime

# ============================================================
# EXISTENTE (sin cambios) - compatibilidad con ritual_3i_mqtt.py
# ============================================================

def get_jdn(year, month, day):
    """Calcula el Número de Día Juliano (JDN) para una fecha dada."""
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    jdn = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    return jdn


def _calc_sak_tahn_waax(jdn):
    """
    Calcula el ciclo Venus-Sol de 2920 días (Sak Tahn Waax).
    5 ciclos sinódicos de Venus (584 días) = 2920 días.
    Retorna la fase exacta del ciclo Venusino.
    """
    ref_jdn = 2451545
    days_passed = jdn - ref_jdn
    grand_cycle_day = days_passed % 2920
    venus_synodic_day = days_passed % 584

    if 0 <= venus_synodic_day < 50:
        phase = "Superior (Tras Sol)"
    elif 50 <= venus_synodic_day < 263:
        phase = "Estrella de la Tarde"
    elif 263 <= venus_synodic_day < 313:
        phase = "Inferior (Frente a Sol/Ocultamiento)"
    else:
        phase = "Estrella de la Mañana"

    return {
        "venus_phase": phase,
        "venus_synodic_day": int(venus_synodic_day),
        "grand_cycle_day": int(grand_cycle_day),
        "cycle_length": 2920
    }


def get_bioconexion_state():
    """Genera el estado cósmico actual para la telemetría."""
    now = datetime.datetime.utcnow()
    jdn = get_jdn(now.year, now.month, now.day)
    return _calc_sak_tahn_waax(jdn)

# ============================================================
# NUEVO (2026-09-08) - Kin completo con ancla GMT
# ============================================================

_ANCLA_GMT = datetime.date(2012, 12, 21)
_ANCLA_TONO = 4
_ANCLA_NAHUAL = 19
_ANCLA_HAAB_IDX = 13 * 20 + 2
_ANCLA_LC_DIAS = 13 * 144000

NOMBRES_TZOLKIN = [
    "Imix", "Ik'", "Ak'b'al", "K'an", "Chicchán", "Kimi", "Manik'",
    "Lamat", "Muluk", "Ok", "Chuwen", "Eb'", "B'en", "Ix", "Men",
    "K'ib", "Kab'an", "Etz'nab'", "Kawak", "Ajaw",
]
NAHUALES_AZTECAS = [
    "Cipactli", "Ehécatl", "Calli", "Cuetzpalin", "Cóatl", "Miquiztli",
    "Máztatl", "Tochtli", "Atl", "Itzcuintli", "Ozomatli", "Malinalli",
    "Ácatl", "Océlotl", "Cuauhtli", "Cozcacuauhtli", "Ollin", "Técpatl",
    "Quiáhuitl", "Xóchitl",
]
MESES_HAAB = [
    "Pop", "Wo'", "Sip", "Sotz'", "Sek", "Xul", "Yaxk'in", "Mol",
    "Ch'en", "Yax", "Sak", "Keh", "Mak", "K'ank'in", "Muwan",
    "Pax", "K'ayab", "Kumk'u", "Wayeb'",
]


def fecha_a_kin_completo(fecha):
    """Convierte una fecha en Tzolk'in, Haab', Cuenta Larga y Kin 1-260."""
    delta = (fecha - _ANCLA_GMT).days
    tono = ((_ANCLA_TONO - 1 + delta) % 13) + 1
    nahual_id = (_ANCLA_NAHUAL + delta) % 20
    kin_260 = next(
        x + 1 for x in range(260)
        if x % 20 == nahual_id and x % 13 == tono - 1
    )
    haab_idx = (_ANCLA_HAAB_IDX + delta) % 365
    haab_dia = haab_idx % 20 + 1
    haab_mes = MESES_HAAB[haab_idx // 20]

    total = _ANCLA_LC_DIAS + delta
    baktun, resto = divmod(total, 144000)
    katun, resto = divmod(resto, 7200)
    tun, resto = divmod(resto, 360)
    uinal, kin = divmod(resto, 20)

    return {
        "fecha": fecha.isoformat(),
        "jdn": get_jdn(fecha.year, fecha.month, fecha.day),
        "tzolkin": {
            "tono": tono,
            "nahual_id": nahual_id,
            "nombre_maya": NOMBRES_TZOLKIN[nahual_id],
            "nahual_azteca": NAHUALES_AZTECAS[nahual_id],
            "kin_260": kin_260,
        },
        "haab": {
            "dia": haab_dia,
            "mes": haab_mes,
            "notacion": "{} {}".format(haab_dia, haab_mes),
        },
        "cuenta_larga": {
            "notacion": "{}.{}.{}.{}.{}".format(baktun, katun, tun, uinal, kin),
            "baktun": baktun,
            "katun": katun,
            "tun": tun,
            "uinal": uinal,
            "kin": kin,
        },
    }


def get_estado_cosmico(fecha=None):
    """Estado extendido. No sustituye get_bioconexion_state() plano."""
    if fecha is None:
        fecha = datetime.date.today()
    jdn = get_jdn(fecha.year, fecha.month, fecha.day)
    estado = _calc_sak_tahn_waax(jdn)
    estado["fecha_gregoriana"] = fecha.isoformat()
    estado["kin_completo"] = fecha_a_kin_completo(fecha)
    return estado
