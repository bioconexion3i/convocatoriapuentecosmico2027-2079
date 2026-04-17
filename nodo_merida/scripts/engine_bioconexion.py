"""
PUENTE CÓSMICO 2027-2079 - NODO FARO MÉRIDA
Protocolo de Sincronía Arqueoastronómica V2
Basado en: Anthony F. Aveni - "Observadores del Cielo en el México Antiguo"
"""

import math
from datetime import datetime

class EngineBioconexion:
    def __init__(self):
        # --- CONSTANTES DE CALIBRACIÓN ---
        self.GMT_CORRELATION = 584283  # Constante GMT
        self.SUPERNUMBER = 1366560     # 9.9.16.0.0 (Armonizador)
        self.LUNAR_CYCLE = 29.530588   # Mes sinódico
        self.VENUS_CYCLE = 583.92      # Ciclo sinódico de Venus
        self.CYCLE_819 = 819           # Ciclo de K'awiil
        
        # Referencias de Época
        self.LUNAR_BASE = datetime(2022, 12, 23)
        self.VENUS_BASE_JDN = 2460169.5  # Conjunción Inferior 2023-08-13

    def get_jdn(self, date_obj):
        """Convierte datetime a Julian Day Number."""
        return (date_obj.timestamp() / 86400) + 2440587.5

    def compute_all_vectors(self, target_date=None):
        if target_date is None:
            target_date = datetime.now()
        
        jdn = self.get_jdn(target_date)
        maya_day = int(jdn - self.GMT_CORRELATION)

        return {
            "timestamp_utc": target_date.isoformat(),
            "long_count": self._calc_long_count(maya_day),
            "harmony_factor": round((maya_day % self.SUPERNUMBER) / self.SUPERNUMBER, 6),
            "lunar_series": self._calc_lunar(target_date),
            "venus_event": self._calc_venus(jdn),
            "kawiil_819": self._calc_819(maya_day)
        }

    def _calc_long_count(self, mdn):
        b, r = divmod(mdn, 144000)
        k, r = divmod(r, 7200)
        t, r = divmod(r, 360)
        u, kin = divmod(r, 20)
        return f"{b}.{k}.{t}.{u}.{kin}"

    def _calc_lunar(self, d):
        age = (d - self.LUNAR_BASE).total_seconds() / 86400 % self.LUNAR_CYCLE
        return {"age": round(age, 2), "phase": "Full" if 14 < age < 16 else "New" if age < 1 or age > 28.5 else "Transit"}

    def _calc_venus(self, jdn):
        day_in_cycle = (jdn - self.VENUS_BASE_JDN) % self.VENUS_CYCLE
        if day_in_cycle < 8: status = "Inferior Conjunction"
        elif day_in_cycle < 244: status = "Morning Star"
        elif day_in_cycle < 334: status = "Superior Conjunction"
        else: status = "Evening Star"
        return {"cycle_day": round(day_in_cycle, 2), "status": status}

    def _calc_819(self, mdn):
        phase = mdn % self.CYCLE_819
        quadrant = phase // 204.75
        colors = ["Red/East", "White/North", "Black/West", "Yellow/South"]
        return {"day": phase, "quadrant_color": colors[int(quadrant)]}

# Ejemplo de uso para el Payload de telemetría
if __name__ == "__main__":
    engine = EngineBioconexion()
    print(engine.compute_all_vectors())
