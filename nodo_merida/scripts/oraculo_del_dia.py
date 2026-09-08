#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Oráculo del Día del Nodo Faro Mérida: JSON, Markdown y MQTT diario."""
import argparse
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

from engine_bioconexion import get_estado_cosmico

TONOS = {1:"unidad y origen",2:"polaridad y reto",3:"ritmo y servicio",4:"medida y forma",5:"centro y empoderamiento",6:"equilibrio orgánico",7:"resonancia y sintonía",8:"justicia armónica",9:"intención y pulso",10:"perfección y manifestación",11:"liberación",12:"cooperación",13:"presencia y trascendencia"}
VERBOS = {1:"nacer",2:"elegir",3:"servir",4:"medir",5:"centrar",6:"equilibrar",7:"resonar",8:"armonizar",9:"pulsar",10:"manifestar",11:"liberar",12:"cooperar",13:"trascender"}
SIGNIFICADOS = ["lagarto","viento","casa","lagartija","serpiente","muerte","venado","conejo","agua","perro","mono","hierba","caña","jaguar","águila","zopilote","movimiento","cuchillo","lluvia","flor"]
ORACULOS = {
0:("el inicio desde el origen","iniciar sin esperar apoyo","dispersión de la energía inicial","agua a la tierra"),1:("el aliento y la comunicación","inspirar y dar palabra","palabra que se dispersa","copal o incienso"),2:("la interioridad y la noche","visión dentro de la oscuridad","miedo a lo no visible","una vela al anochecer"),3:("la siembra y el sustento","fertilidad: hacer crecer","apego al fruto cultivado","semillas a la tierra"),4:("la energía y el cosmos","transformar la fuerza vital","sobre-identificación con el poder","movimiento consciente"),5:("el soltar y renovar","cerrar ciclos con gratitud","resistencia al cambio","dejar ir algo material"),6:("el servicio y la ofrenda","sanar con las propias manos","auto-sacrificio excesivo","compartir una herramienta"),7:("la armonía y la guía","señalar el camino sin imponer","vanidad de la propia luz","luz a otro ser"),8:("el flujo emocional","purificar lo que estanca","mareas emocionales descontroladas","agua en movimiento"),9:("la lealtad y el acompañamiento","guiar hasta el otro lado","dependencia afectiva","compañía a quien la necesita"),10:("el arte y el juego","crear con alegría","burla o frivolización","una pequeña obra"),11:("el camino compartido","abrir veredas para otros","perder el propio camino","un paso dado por otro"),12:("la dirección y el eje","sostener el centro del grupo","autoridad rígida","una caña o maíz"),13:("el poder silencioso de la tierra","intuición y magia práctica","manipulación sutil","silencio en la naturaleza"),14:("la visión de conjunto","ver desde la altura","arrogancia de perspectiva","contemplar el horizonte"),15:("la memoria y la limpieza","sanar los recuerdos","aferrarse al pasado","limpiar un espacio"),16:("el cambio y el temblor","sincronía con el movimiento","agitación sin rumbo","danza consciente"),17:("la verdad y el corte","precisión que libera","herir con la verdad","una decisión limpia"),18:("la tormenta colectiva","traer la lluvia que renueva","caos interior","resistencia serena"),19:("la luz del liderazgo","iluminar sin quemar","ego del cargo","gratitud al sol")}

def generar_oraculo(fecha):
    estado = get_estado_cosmico(fecha); k = estado["kin_completo"]
    tono = k["tzolkin"]["tono"]; nombre = k["tzolkin"]["nombre_maya"]
    tema, don, sombra, ofrenda = ORACULOS[k["tzolkin"]["nahual_id"]]
    return {"fecha":estado["fecha_gregoriana"],"jdn":k["jdn"],"kin":"{} {}".format(tono,nombre),"kin_260":k["tzolkin"]["kin_260"],"haab":k["haab"]["notacion"],"cuenta_larga":k["cuenta_larga"]["notacion"],"venus":{"fase":estado["venus_phase"],"dia_sinodico":estado["venus_synodic_day"],"gran_ciclo":estado["grand_cycle_day"],"ciclo_total":estado["cycle_length"]},"tono_sentido":TONOS[tono],"nahual_significado":SIGNIFICADOS[k["tzolkin"]["nahual_id"]],"tema":tema,"don":don,"sombra":sombra,"ofrenda":ofrenda,"mantra":"Como {}, el tono {} ({}) invita a {}: {}.".format(nombre,tono,TONOS[tono],VERBOS[tono],don)}

def generar_markdown(o):
    v=o["venus"]
    return "# 🌞 Oráculo del Día — {fecha}\n\n## {kin} — {nahual_significado}\n\n> {mantra}\n\n| Elemento | Valor |\n|---|---|\n| Kin | {kin} ({kin_260}/260) |\n| Haab' | {haab} |\n| Cuenta Larga | {cuenta_larga} |\n| Venus | {fase} (día {dia_sinodico}/584, ciclo {gran_ciclo}/{ciclo_total}) |\n| Tono {tono} | {tono_sentido} |\n\n## 🌱 Don\n{don}\n\n## 🌑 Sombra a vigilar\n{sombra}\n\n## 🔥 Ofrenda sugerida\n{ofrenda}\n".format(tono=o["kin"].split(" ")[0],fase=v["fase"],dia_sinodico=v["dia_sinodico"],gran_ciclo=v["gran_ciclo"],ciclo_total=v["ciclo_total"],**o)

def publicar_mqtt(payload, topic):
    try:
        import paho.mqtt.client as mqtt
    except ImportError:
        print("[mqtt] paho-mqtt no instalado; se omite publicación", file=sys.stderr); return False
    try:
        cliente=mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2,client_id="oraculo_del_dia")
        user=os.environ.get("MQTT_USER",""); password=os.environ.get("MQTT_PASSWORD","")
        if user and password: cliente.username_pw_set(user,password)
        cliente.connect(os.environ.get("MQTT_BROKER","127.0.0.1"),int(os.environ.get("MQTT_PORT","1883")),keepalive=30)
        cliente.loop_start(); info=cliente.publish(topic,json.dumps(payload,ensure_ascii=False),qos=1); info.wait_for_publish(timeout=10); cliente.loop_stop(); cliente.disconnect()
        return info.rc==0
    except Exception as exc:
        print("[mqtt] error publicando en {}: {}".format(topic,exc),file=sys.stderr); return False

def ejecutar(fecha,out_dir,topic,nodo_id):
    o=generar_oraculo(fecha); out_dir.mkdir(parents=True,exist_ok=True)
    (out_dir/(fecha.isoformat()+".json")).write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding="utf-8")
    (out_dir/(fecha.isoformat()+".md")).write_text(generar_markdown(o),encoding="utf-8")
    print(generar_markdown(o)); payload=dict(o); payload.update({"nodo_id":nodo_id,"tipo":"oraculo_diario","nahual":{"es":o["kin"].split(" ",1)[1]}})
    ok=publicar_mqtt(payload,topic); print("[mqtt] {} en {}".format("publicado" if ok else "omitido",topic)); return o

def segundos_hasta_hora(hora,tz_name):
    from zoneinfo import ZoneInfo
    ahora=dt.datetime.now(ZoneInfo(tz_name)); objetivo=ahora.replace(hour=hora,minute=0,second=0,microsecond=0)
    if objetivo<=ahora: objetivo+=dt.timedelta(days=1)
    return (objetivo-ahora).total_seconds()

def main():
    p=argparse.ArgumentParser(description="Oráculo del Día (Stardust)"); g=p.add_mutually_exclusive_group(); g.add_argument("--hoy",action="store_true"); g.add_argument("--fecha")
    p.add_argument("--out",default="salida"); p.add_argument("--topic",default="stardust/merida/evento"); p.add_argument("--nodo",default=None); p.add_argument("--loop",action="store_true"); p.add_argument("--hora",type=int,default=6); p.add_argument("--tz",default="America/Merida")
    a=p.parse_args(); fecha=dt.date.fromisoformat(a.fecha) if a.fecha else dt.date.today(); nodo=a.nodo or os.environ.get("NODO_ID","merida-avenida-yucatan-orin")
    if not a.loop: ejecutar(fecha,Path(a.out),a.topic,nodo); return
    while True:
        ejecutar(dt.date.today(),Path(a.out),a.topic,nodo); time.sleep(segundos_hasta_hora(a.hora,a.tz))
if __name__=="__main__": main()
