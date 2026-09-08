#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pruebas GMT, compatibilidad del faro y Kin completo."""
import datetime as dt
from engine_bioconexion import get_jdn,_calc_sak_tahn_waax,get_bioconexion_state,fecha_a_kin_completo,get_estado_cosmico

def kin_de(f): return fecha_a_kin_completo(f)
def test_ancla_gmt_2012():
 k=kin_de(dt.date(2012,12,21)); assert (k["tzolkin"]["tono"],k["tzolkin"]["nombre_maya"],k["haab"]["notacion"],k["cuenta_larga"]["notacion"],k["tzolkin"]["kin_260"])==(4,"Ajaw","3 K'ank'in","13.0.0.0.0",160)
def test_latido_nodo_2026():
 k=kin_de(dt.date(2026,9,4)); v=_calc_sak_tahn_waax(get_jdn(2026,9,4)); assert (k["tzolkin"]["tono"],k["tzolkin"]["nombre_maya"],k["haab"]["notacion"],k["cuenta_larga"]["notacion"],v["venus_synodic_day"],v["grand_cycle_day"],v["venus_phase"])==(4,"Chicchán","18 Mol","13.0.13.16.5",399,983,"Estrella de la Mañana")
def test_kin_natal_2003():
 k=kin_de(dt.date(2003,9,4)); assert (k["tzolkin"]["tono"],k["tzolkin"]["nombre_maya"],k["haab"]["notacion"],k["cuenta_larga"]["notacion"],k["tzolkin"]["kin_260"])==(1,"K'an","12 Mol","12.19.10.10.4",144)
def test_coherencia_8401_dias():
 d=(dt.date(2026,9,4)-dt.date(2003,9,4)).days; assert d==8401 and d%13==3 and d%20==1
def test_nahual_formula_ritual():
 for f in [dt.date(2003,9,4),dt.date(2012,12,21),dt.date(2026,9,4),dt.date(2026,9,8)]: assert kin_de(f)["tzolkin"]["nahual_id"]==(get_jdn(f.year,f.month,f.day)-584283+19)%20
def test_jdn_canonico():
 for f in [dt.date(2000,1,1),dt.date(2012,12,21),dt.date(1987,1,1),dt.date(2026,9,4)]: assert get_jdn(f.year,f.month,f.day)==f.toordinal()+1721425
def test_bioconexion_state_forma_plana():
 e=get_bioconexion_state(); assert all(c in e for c in ("venus_phase","venus_synodic_day","grand_cycle_day","cycle_length")) and e["cycle_length"]==2920
def test_estado_cosmico_extendido():
 e=get_estado_cosmico(dt.date(2026,9,4)); assert e["kin_completo"]["tzolkin"]["nombre_maya"]=="Chicchán" and "venus_phase" in e
def test_avance_diario():
 f=dt.date(2026,9,4); a,b=kin_de(f),kin_de(f+dt.timedelta(days=1)); assert b["tzolkin"]["nahual_id"]==(a["tzolkin"]["nahual_id"]+1)%20 and b["tzolkin"]["tono"]==(a["tzolkin"]["tono"]%13)+1
if __name__=="__main__":
 pruebas=[v for k,v in sorted(globals().items()) if k.startswith("test_") and callable(v)]; fallos=0
 for prueba in pruebas:
  try: prueba(); print("  OK    {}".format(prueba.__name__))
  except AssertionError: fallos+=1; print("  FALLO {}".format(prueba.__name__))
 print("\n{}/{} pruebas pasadas".format(len(pruebas)-fallos,len(pruebas))); raise SystemExit(1 if fallos else 0)
