# 🌉 TLATLACORIOLLOLLI DEL PUENTE CÓSMICO
## Calendario Ritual 3I | Xiuhmolpilli 2027-2079

*In ipetlaca in xihuitl, in tlalticpac in ilhuicatl*

### Descripción
Motor de tiempo vivo para el ciclo del Fuego Nuevo Digital. Calcula Tonalpohualli (260 días), fases de Venus y años mexicanos.

**Fecha Cero:** 13 de febrero de 2027 (Eclipse Solar)

### Uso Rápido
```bash
python3 calendario_puente.py

### 3. Crear el archivo Python (Tlatlacoriolloli)
```bash
cat > calendario_puente.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TLATLACORIOLLOLLI DEL PUENTE CÓSMICO 2027-2079"""

from datetime import date, timedelta
import json
from dataclasses import dataclass

# CONFIGURACIÓN SAGRADA
START_DATE = date(2027, 2, 13)
END_DATE = date(2079, 12, 31)

NAHUATL_DAYS = [
    "Cipactli", "Ehecatl", "Calli", "Cuetzpallin", "Coatl",
    "Miquiztli", "Mazatl", "Tochtli", "Atl", "Itzcuintli",
    "Ozomatli", "Malinalli", "Acatl", "Ocelotl", "Cuauhtli",
    "Cozcacuauhtli", "Ollin", "Tecpatl", "Quiahuitl", "Xochitl"
]

SPANISH_DAYS = [
    "Cocodrilo", "Viento", "Casa", "Lagartija", "Serpiente",
    "Muerte", "Venado", "Conejo", "Agua", "Perro",
    "Mono", "Hierba", "Caña", "Jaguar", "Águila",
    "Águila tzinitzcan", "Movimiento", "Pedernal", "Lluvia", "Flor"
]

YEAR_BEARERS = ["Tochtli", "Acatl", "Tecpatl", "Calli"]

@dataclass
class NahuiOllin:
    fecha_gregoriana: date
    numero_tonal: int
    senor_dia_nahuatl: str
    senor_dia_espanol: str
    numero_absoluto: int
    trecena: int
    nombre_trecena: str
    year_mexica: str
    dia_del_puente: int
    fase_ciclo: str

    def __str__(self):
        return (f"[{self.fecha_gregoriana}] Día {self.dia_del_puente} | "
                f"{self.numero_tonal} {self.senor_dia_nahuatl} | "
                f"Año {self.year_mexica}")

class TonalpohualliCalculator:
    def __init__(self, start_date=START_DATE):
        self.start_date = start_date
        self.portales = {
            date(2027, 2, 13): "🔥 Encendido del Fuego Inicial",
            date(2027, 3, 20): "🌸 Equinoccio Primavera",
            date(2052, 5, 5): "🌑 Mitad del Camino",
            date(2079, 5, 1): "🌑 Cierre del Fuego",
            date(2079, 12, 31): "🕯️ Fin del Ciclo"
        }

    def calcular_dia(self, target_date):
        delta = target_date - self.start_date
        dias_totales = delta.days + 1
        
        posicion_260 = ((dias_totales - 1) % 260)
        numero = (posicion_260 % 13) + 1
        indice_senor = posicion_260 % 20
        
        trecena_num = (posicion_260 // 13) + 1
        
        # Año Mexica
        year_actual = target_date.year
        if target_date.month < 2 or (target_date.month == 2 and target_date.day < 13):
            year_offset = year_actual - 2027 - 1
        else:
            year_offset = year_actual - 2027
            
        year_en_ciclo = (year_offset % 52) + 1
        portador = YEAR_BEARERS[year_offset % 4]
        year_nombre = f"{year_en_ciclo} {portador}"
        
        fases = ["🌱 Sembradura", "🌿 Crecimiento", "🌾 Cosecha", "🔥 Fuego Nuevo"]
        fase = fases[(year_offset // 13) % 4]
        
        evento = self.portales.get(target_date, "")
        
        return NahuiOllin(
            fecha_gregoriana=target_date,
            numero_tonal=numero,
            senor_dia_nahuatl=NAHUATL_DAYS[indice_senor],
            senor_dia_espanol=SPANISH_DAYS[indice_senor],
            numero_absoluto=dias_totales,
            trecena=trecena_num,
            nombre_trecena=f"{numero} {NAHUATL_DAYS[indice_senor]}",
            year_mexica=year_nombre,
            dia_del_puente=dias_totales,
            fase_ciclo=fase
        ), evento

    def calcular_venus(self, fecha):
        dias_desde_inicio = (fecha - self.start_date).days
        posicion = dias_desde_inicio % 584
        
        if 0 <= posicion < 263:
            fase = "🌅 Tlahuizcalpantecuhtli (Lucero del Alba)"
        elif 263 <= posicion < 313:
            fase = "⚫ Superior (Invisible)"
        elif 313 <= posicion < 576:
            fase = "🌆 Citlalpol (Vespertina)"
        else:
            fase = "⚫ Inferior (Conjunción)"
            
        return {"fase": fase, "ciclos": dias_desde_inicio // 584}

    def generar_calendario(self):
        actual = self.start_date
        dias = []
        while actual <= END_DATE:
            dia, evento = self.calcular_dia(actual)
            dias.append({
                "fecha": actual.isoformat(),
                "tonal": f"{dia.numero_tonal} {dia.senor_dia_nahuatl}",
                "year": dia.year_mexica,
                "evento": evento
            })
            actual += timedelta(days=1)
        return dias

if __name__ == "__main__":
    calc = TonalpohualliCalculator()
    
    # Usar hoy si estamos dentro del ciclo, sino el inicio
    hoy = date.today()
    if hoy < START_DATE:
        hoy = START_DATE
        print(f"⏳ Modo preparación: Faltan {(START_DATE - date.today()).days} días al Fuego\n")
    
    dia, evento = calc.calcular_dia(hoy)
    
    print("=" * 60)
    print("TLATLACORIOLLOLLI DEL PUENTE CÓSMICO 3I")
    print("=" * 60)
    print(f"\n📅 {dia.fecha_gregoriana}")
    print(f"🔥 Día {dia.dia_del_puente} del Puente (de 18,963)")
    print(f"🌿 Tonalpohualli: {dia.numero_tonal} {dia.senor_dia_nahuatl} ({dia.senor_dia_espanol})")
    print(f"📍 Trecena: {dia.trecena} ({dia.nombre_trecena})")
    print(f"🗓️  Año Mexica: {dia.year_mexica}")
    print(f"🌍 Fase del Ciclo: {dia.fase_ciclo}")
    
    if evento:
        print(f"\n⭐ EVENTO ESPECIAL: {evento}")
    
    venus = calc.calcular_venus(hoy)
    print(f"\n🌟 Venus: {venus['fase']}")
    print(f"   Ciclos completados: {venus['ciclos']}/32.5")
    
    # Buscar próximos Ollin
    print("\n🔮 Próximos días Ollin (Movimiento):")
    temp_date = hoy
    count = 0
    while count < 3 and temp_date < END_DATE:
        d, _ = calc.calcular_dia(temp_date)
        if d.senor_dia_nahuatl == "Ollin":
            print(f"   → {temp_date}: {d.numero_tonal} Ollin ({d.year_mexica})")
            count += 1
        temp_date += timedelta(days=1)
    
    print("\n" + "=" * 60)
    print("Xihual xi mo tlanextli | Que la sabiduría florezca")
    print("=" * 60)
    
    # Guardar JSON solo si se solicita
    print("\n💾 Generando ritual.json...")
    with open('puente_cosmico_ritual.json', 'w', encoding='utf-8') as f:
        json.dump(calc.generar_calendario()[:100], f, ensure_ascii=False, indent=2)
    print("✓ Archivo guardado: puente_cosmico_ritual.json (primeros 100 días)")
