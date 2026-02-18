#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date, timedelta
import json
import sys

# CONFIGURACION SAGRADA DEL PUENTE
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
    "Mono", "Hierba", "Cana", "Jaguar", "Aguila",
    "Aguila tzinitzcan", "Movimiento", "Pedernal", "Lluvia", "Flor"
]

YEAR_BEARERS = ["Tochtli", "Acatl", "Tecpatl", "Calli"]

class TonalpohualliCalculator:
    def __init__(self):
        self.portales = {
            date(2027, 2, 13): "Encendido del Fuego Inicial",
            date(2027, 3, 20): "Equinoccio Primavera",
            date(2052, 5, 5): "Mitad del Camino - 1 Coatl",
            date(2079, 5, 1): "Cierre del Fuego",
            date(2079, 12, 31): "Fin del Ciclo"
        }
    
    def calcular_dia(self, target_date):
        delta = target_date - START_DATE
        dias_totales = delta.days + 1
        
        # Posicion en ciclo de 260
        posicion_260 = ((dias_totales - 1) % 260)
        numero = (posicion_260 % 13) + 1
        indice_senor = posicion_260 % 20
        trecena_num = (posicion_260 // 13) + 1
        
        # Calculo de ano mexica
        year_actual = target_date.year
        if target_date.month < 2 or (target_date.month == 2 and target_date.day < 13):
            year_offset = year_actual - 2027 - 1
        else:
            year_offset = year_actual - 2027
        
        year_en_ciclo = (year_offset % 52) + 1
        portador = YEAR_BEARERS[year_offset % 4]
        
        # Fases del ciclo 52-anos
        fases = ["Sembradura", "Crecimiento", "Cosecha", "Fuego Nuevo"]
        fase = fases[(year_offset // 13) % 4]
        
        evento = self.portales.get(target_date, "")
        senor = NAHUATL_DAYS[indice_senor]
        
        return {
            "fecha": str(target_date),
            "dia_puente": dias_totales,
            "tonal_num": numero,
            "tonal_nombre": senor,
            "tonal_espanol": SPANISH_DAYS[indice_senor],
            "trecena": trecena_num,
            "year_mexica": f"{year_en_ciclo} {portador}",
            "fase_ciclo": fase,
            "evento": evento
        }
    
    def calcular_venus(self, fecha):
        dias = (fecha - START_DATE).days
        pos = dias % 584
        
        if 0 <= pos < 263:
            fase = "Tlahuizcalpantecuhtli (Lucero del Alba)"
        elif 263 <= pos < 313:
            fase = "Superior (Invisible)"
        elif 313 <= pos < 576:
            fase = "Citlalpol (Vespertina)"
        else:
            fase = "Inferior (Conjuncion)"
        
        return {"fase": fase, "ciclos_completos": dias // 584}

if __name__ == "__main__":
    calc = TonalpohualliCalculator()
    
    # Determinar fecha a consultar
    hoy = date.today()
    if hoy < START_DATE:
        hoy = START_DATE
        dias_faltan = (START_DATE - date.today()).days
        print(f"[Modo Preparacion] Faltan {dias_faltan} dias al Fuego Inicial\n")
    
    resultado = calc.calcular_dia(hoy)
    venus = calc.calcular_venus(hoy)
    
    # Mostrar resultados
    print("=" * 55)
    print("TLATLACORIOLLOLLI DEL PUENTE COSMICO 3I")
    print("=" * 55)
    print(f"Fecha Gregoriana: {resultado['fecha']}")
    print(f"Dia del Puente: {resultado['dia_puente']} / 18,963")
    print(f"Tonalpohualli: {resultado['tonal_num']} {resultado['tonal_nombre']}")
    print(f"  ({resultado['tonal_espanol']})")
    print(f"Trecena: {resultado['trecena']} de 20")
    print(f"Ano Mexica: {resultado['year_mexica']}")
    print(f"Fase: {resultado['fase_ciclo']}")
    
    if resultado['evento']:
        print(f"\nEVENTO ESPECIAL: {resultado['evento']}")
    
    print(f"\nVenus: {venus['fase']}")
    print(f"Ciclos: {venus['ciclos_completos']}/32.5")
    print("=" * 55)
    
    # Guardar JSON si se pide
    if "--json" in sys.argv:
        import json
        with open('tonal_hoy.json', 'w') as f:
            json.dump(resultado, f, indent=2)
        print("Archivo guardado: tonal_hoy.json")
