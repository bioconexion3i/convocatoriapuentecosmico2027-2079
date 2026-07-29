import datetime

def get_jdn(year, month, day):
    """Calcula el Número de Día Juliano (JDN) para una fecha dada."""
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    jdn = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    return jdn

def _calc_sak_tahn_waax(jdn):
    """
    Calcula el ciclo Venus-Sol de 2920 dias (Sak Tahn Waax).
    5 ciclos sinodicos de Venus (584 dias) = 2920 dias.
    Retorna la fase exacta del ciclo Venusino.
    """
    # Referencia: 1 Enero 2000 (JDN 2451545) como punto base sincronizado
    ref_jdn = 2451545
    days_passed = jdn - ref_jdn
    
    # Posición en el gran ciclo de 2920 días
    grand_cycle_day = days_passed % 2920
    # Posición en el ciclo sinódico individual de Venus (584 días)
    venus_synodic_day = days_passed % 584
    
    # Determinar la fase de Venus
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
