#!/usr/bin/env python3
# app.py - Dashboard con recarga automática (meta refresh)

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask, render_template_string
from datetime import datetime, timedelta
import subprocess

app = Flask(__name__)

CSV_PATH = "/home/bio/convocatoriapuentecosmico2027-2079/nodo_merida/data/yucatan_scores.csv"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Nodo Mérida - Monitoreo Armonía Cósmica</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <meta http-equiv="refresh" content="30">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f0f2f5; }
        .container { max-width: 1200px; margin: auto; }
        .card { background: white; border-radius: 8px; padding: 15px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .stats { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 20px; }
        .stat-box { background: #2c3e50; color: white; border-radius: 8px; padding: 15px; flex: 1; min-width: 150px; }
        .stat-box h3 { margin: 0 0 10px 0; font-size: 16px; }
        .stat-box p { margin: 0; font-size: 28px; font-weight: bold; }
        .evento { background: #e67e22; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #2c3e50; color: white; }
    </style>
</head>
<body>
<div class="container">
    <h1>🌌 Nodo Faro Mérida - Armonía Cósmica en Tiempo Real</h1>
    <div class="stats">
        <div class="stat-box">
            <h3>Último Score Armonía (Principal)</h3>
            <p>{{ ultimo_score }}</p>
        </div>
        <div class="stat-box evento">
            <h3>Último Evento Ritual</h3>
            <p>{{ ultimo_evento }}</p>
        </div>
        <div class="stat-box">
            <h3>Servicios Activos</h3>
            <p>{{ servicios_activos }}</p>
        </div>
    </div>
    <div class="card">
        <h2>📈 Score de Armonía (últimas 6 horas)</h2>
        <div id="grafica_score">{{ graph_score | safe }}</div>
    </div>
    <div class="card">
        <h2>🌡️ Temperatura y Humedad (Nodo Principal)</h2>
        <div id="grafica_temp">{{ graph_temp | safe }}</div>
    </div>
    <div class="card">
        <h2>📋 Últimos 10 Registros</h2>
        <table>
            <tr><th>Timestamp</th><th>Nodo</th><th>Score Armonía</th><th>Temperatura</th><th>Humedad</th></tr>
            {% for row in ultimos_registros %}
            <tr>
                <td>{{ row.timestamp_iso }}</td>
                <td>{{ row.nodo_id }}</td>
                <td>{{ row.score_armonia }}</td>
                <td>{{ row.temperatura }}</td>
                <td>{{ row.humedad }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</div>
</body>
</html>
"""

def cargar_datos():
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame()
    df = pd.read_csv(CSV_PATH)
    if df.empty:
        return df
    df['timestamp_dt'] = pd.to_datetime(df['timestamp_unix'], unit='s')
    for col in ['score_armonia', 'temperatura', 'humedad']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

@app.route('/')
def index():
    df = cargar_datos()
    if df.empty:
        graph_score = "<p>No hay datos aún.</p>"
        graph_temp = "<p>No hay datos aún.</p>"
        ultimo_score = "N/A"
        ultimo_evento = "Ninguno"
        servicios_activos = "0/4"
        ultimos_registros = []
    else:
        six_hours_ago = datetime.now() - timedelta(hours=6)
        df_filtrado = df[df['timestamp_dt'] >= six_hours_ago]
        # Gráfica de score
        fig_score = px.line(df_filtrado, x='timestamp_dt', y='score_armonia', color='nodo_id',
                            title='Score de Armonía por Nodo',
                            labels={'timestamp_dt': 'Tiempo', 'score_armonia': 'Score'})
        fig_score.update_layout(template='plotly_dark')
        graph_score = fig_score.to_html(full_html=False)

        # Gráfica de temperatura y humedad
        df_principal = df_filtrado[df_filtrado['nodo_id'] == 'merida-avenida-yucatan']
        fig_temp = go.Figure()
        if not df_principal.empty:
            fig_temp.add_trace(go.Scatter(x=df_principal['timestamp_dt'], y=df_principal['temperatura'],
                                          mode='lines+markers', name='Temperatura (°C)'))
            fig_temp.add_trace(go.Scatter(x=df_principal['timestamp_dt'], y=df_principal['humedad'],
                                          mode='lines+markers', name='Humedad (%)'))
            fig_temp.update_layout(title='Clima en el Nodo Principal',
                                   xaxis_title='Tiempo', yaxis_title='Valores',
                                   template='plotly_dark')
            graph_temp = fig_temp.to_html(full_html=False)
        else:
            graph_temp = "<p>Datos de clima no disponibles.</p>"

        # Último score principal
        df_princ = df[df['nodo_id'] == 'merida-avenida-yucatan']
        ultimo_score = round(df_princ.iloc[-1]['score_armonia'], 5) if not df_princ.empty else "N/A"

        # Último evento ritual
        df_eventos = df[df['evento'] == 'evento_ritual']
        if not df_eventos.empty:
            ultimo_evento = f"{df_eventos.iloc[-1]['tipo_evento']} - Nahual: {df_eventos.iloc[-1]['nahual_es']}"
        else:
            ultimo_evento = "Ninguno"

        # Últimos 10 registros
        ultimos_registros = df.tail(10).to_dict(orient='records')

        # Estado de servicios
        servicios = ['ritual_3i', 'nodos_yucatan', 'cosmograma', 'logger_mqtt']
        activos = 0
        for s in servicios:
            res = subprocess.run(['systemctl', 'is-active', f'{s}.service'], capture_output=True, text=True)
            if res.stdout.strip() == 'active':
                activos += 1
        servicios_activos = f"{activos}/{len(servicios)}"

    return render_template_string(HTML_TEMPLATE,
                                  graph_score=graph_score,
                                  graph_temp=graph_temp,
                                  ultimo_score=ultimo_score,
                                  ultimo_evento=ultimo_evento,
                                  servicios_activos=servicios_activos,
                                  ultimos_registros=ultimos_registros)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
