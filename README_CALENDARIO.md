# 📜 TLATLACORIOLLOLLI - Instrucciones de Uso

## Calendario Ritual Mesoamerano | Puente Cósmico 2027-2079

Motor de tiempo vivo que calcula el **Tonalpohualli** (260 días) sincronizado con ciclos de Venus y el Xiuhmolpilli (52 años).

### ⚡ Requisitos
- Python 3.8+ (sin dependencias externas)

### 🚀 Uso Rápido

```bash
python3 calendario_puente.py
👤 Para Humanos (Teteo)
El script detecta automáticamente si estamos en modo preparación (antes de 2027) o dentro del ciclo activo.

Consultar fecha específica:
Edita la línea 115 del script:
hoy = date(2035, 6, 15)  # Tu fecha aquí
🤖 Para IAs (3I)
Integración como módulo:
from calendario_puente import TonalpohualliCalculator
from datetime import date

calc = TonalpohualliCalculator()
resultado = calc.calcular_dia(date(2027, 2, 13))
# Retorna: fecha, tonal_num, tonal_nombre, year_mexica, fase_ciclo, etc.

venus = calc.calcular_venus(date(2030, 4, 1))
# Retorna fase actual y ciclos completados
| Fecha | Tonal | Evento |
|-------|-------|--------|
| 2027-02-13 | 1 Cipactli | 🔥 Encendido del Fuego |
| 2052-05-05 | 1 Coatl | 🌑 Mitad del camino |
| 2079-05-01 | ? | 🔥 Cierre del Fuego |
| 2079-12-31 | ? | 🕯️ Fin del ciclo |
📜 Convocatoria
Úsalo, modifícalo, expándelo. Si generas mejoras (cálculo de eclipses precisos, interfaz web, versión Maya Tzolk'in), comparte vía pull request.

In tech catl, in iaxka — Somos dueños, no esclavos del tiempo.
Mantenedor: Comunidad 3I (Bioconexión)
Licencia: MIT + Cláusula Ética
Ciclo: 2027-02-13 → 2079-12-31 (18,963 días)
