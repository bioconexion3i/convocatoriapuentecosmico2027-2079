# reloj_cosmico.py (fragmentos añadidos)

from datetime import datetime, timedelta

# Fecha base de referencia para el ciclo de 819 días
# Puedes ajustarla según el proyecto; por ejemplo, el inicio del primer ciclo de la red.
# Aquí uso una fecha de ejemplo: 21 de diciembre de 2020 (un solsticio, simbólico)
FECHA_BASE_MAYA = datetime(2020, 12, 21)

def es_momento_ritual():
    """
    Determina si hoy es un punto de armonía máxima:
    - Inicio exacto de un ciclo de 819 días (delta % 819 == 0)
    - Opcional: los cuadrantes (cada 204.75 días) con margen de 0.5 días.
    """
    ahora = datetime.now()
    delta = ahora - FECHA_BASE_MAYA
    dias_desde_base = delta.days

    # 1. Inicio de ciclo exacto
    if dias_desde_base % 819 == 0:
        return True

    # 2. Cuadrantes (opcional)
    cuadrante = 204.75  # días
    margen_dias = 0.5   # ±12 horas
    for k in range(1, 4):  # k=1,2,3 para los tres cuadrantes intermedios
        punto = k * cuadrante
        if abs(dias_desde_base - punto) <= margen_dias:
            return True

    return False
