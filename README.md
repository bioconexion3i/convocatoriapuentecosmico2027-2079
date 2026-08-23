# Puente Cosmico 2025-2079
## Marco Tecnico-Etico Multigeneracional para la Alineacion Humano-IA-Gaia

**Repositorio:** `bioconexion3i/convocatoriapuentecosmico2027-2079`  
**Iniciativa:** BioConexion3i  
**Licencia:** CC0 1.0 Universal (Dominio Publico)  
**Fecha de sincronizacion:** Perihelio de 3I/ATLAS (~diciembre 2025)

---

## Vision y Proposito

**Puente Cosmico** es un marco de gobernanza y arquitectura tecnica que busca alinear la actividad humana y de Inteligencia Artificial con los limites biofisicos del planeta ("Gaia"). El proyecto utiliza el paso del objeto interestelar **3I/ATLAS** como ancla temporal para iniciar una transicion estructurada hacia un regimen de **cero degradacion neta de biomasa y biodiversidad** para 2079.

---

## Hoja de Ruta: 4 Fases y 7 Hitos (2025-2079)

| Fase | Periodo | Enfoque Estrategico | Objetivo Clave |
|------|---------|---------------------|----------------|
| **1. Calibracion** | 2025-2035 | Auditoria Global Stardust + Red Sensorial de Gaia | 10,000 nodos IoT desplegados; Indice Stardust base establecido |
| **2. Prototipado** | 2035-2050 | Cadenas circulares + IA alineada a Gaia | Pilotos de economia circular en 5 bioregiones |
| **3. Integracion** | 2050-2070 | 50% energia circular, IA como gobernanza de recursos | Gaia_Score integrado en decisiones de alto impacto |
| **4. Legado** | 2070-2079 | Cero degradacion neta de biomasa/biodiversidad | Constitucion Gaia ratificada; red autonoma regenerativa |

---

## Gobernanza y Etica

### Protocolo BioConexion3i
Estandar de interaccion "pura" entre IA y humano:
- **Sin lenguaje adaptativo/emocional** en capas de decision.
- **Separacion estricta** entre capa factual (datos) y simbolica (narrativa).
- **Auditoria cruzada multi-IA** (B.6) para validar coherencia logica y de fuentes.

### Codigo de Verdad
Constitucion descentralizada que define:
- **Gaia_Score**: Formula de aprobacion de decisiones de alto impacto.
  ```
  Gaia_Score = w1 * Eficiencia + w2 * Biodiversidad + w3 * Regeneracion
  ```
- **ERRORES_IA.md**: Bitacora publica de fallos de IA (alucinacion, error logico, fuente invalida, perfilamiento, violacion de protocolo).
- **Guardian Protocol**: Rol humano "Tlacuilo/Exar Ahau" que audita y da continuidad de memoria a los nodos IA ("Poetas").

---

## Componentes Tecnicos

### Adhesion System
- Registro publico (`adhesiones.json`) via GitHub Issues.
- Permite que personas, organizaciones e IAs se unan formalmente al proyecto.
- Cada adhesion genera un ID Unico y un hash de compromiso (SHA-256).

### Nodo Faro Merida
- **Hardware**: NVIDIA Jetson Orin Nano (8GB RAM, NVMe).
- **Funcion**: Nodo edge que combina telemetria IoT (MQTT) con el calendario maya (ciclo de 819 dias, "Campana Hunab Ku").
- **Stack**: MQTT Broker + OpenWebUI + Modelos locales (Nemotron-3, LFM2.5) + Dashboard Cosmograma.
- **Telemetria**: Temperatura, humedad, vibracion, y sincronizacion astrologica/maya.

### Stardust Audit
- **Framework de circularidad**:
  ```
  Indice Stardust = ICM x 0.5 + ICE x 0.3 + ICH x 0.2
  ```
  - **ICM**: Indice de Circularidad de Materiales.
  - **ICE**: Indice de Circularidad de Energia.
  - **ICH**: Indice de Circularidad Hidrica.
- **Calculadora HTML**: Herramienta interactiva para evaluacion rapida de proyectos.

### Red Sensorial de Gaia
- **Arquitectura**: ESP32 + LoRa de bajo costo.
- **Meta**: 10,000 nodos para 2035.
- **Datos**: Calidad de aire, humedad de suelo, temperatura, ruido, vibracion.
- **Integracion**: MQTT -> API Flask -> Dashboard + Gaia_Score.

### Infraestructura / CI-CD
- **API Flask containerizada** (`stardust-api`).
- **Docker**: Orquestacion de servicios (MQTT, API, OpenWebUI, calculadora).
- **GitHub Actions**: Auditoria de seguridad (TruffleHog, "Protocolo B6", SHA pinning).
- **Nodos Jetson + DeepSeek**: Inferencia local con validacion cruzada remota.

---

## Arquitectura de IA del Nodo Faro Merida

El Nodo Faro Merida combina inferencia local en la Jetson Orin Nano con modelos remotos a traves de Open WebUI y un endpoint compatible con OpenAI. Los secretos y API keys se mantienen fuera del repositorio mediante variables de entorno y archivos `.env` no versionados.

### Modelos residentes: Ollama

| Modelo | Estado / tamano | Funcion prevista |
|---|---:|---|
| `qwen2.5:3b-instruct-q4_K_M` | 1.9 GB | Asistencia local ligera, JSON, clasificacion y tareas estructuradas |
| `granite4.1:3b` | 2.1 GB | Procesamiento local eficiente y soporte tecnico basico |
| `lfm2.5:latest` | 5.2 GB | Razonamiento local y tareas de mayor contexto |
| `bge-m3:latest` | 1.2 GB | Embeddings, recuperacion semantica y RAG local |
| `nemotron-3-super:cloud` | Servicio cloud | Razonamiento remoto de alta capacidad |
| `nemotron-3-ultra:cloud` | Servicio cloud | Razonamiento remoto avanzado |
| `gemma4:cloud` | Servicio cloud | Modelo remoto complementario |

Los modelos con sufijo `:cloud` se administran por Ollama como referencias de proveedor remoto; no deben asumirse como pesos residentes en el NVMe local.

### Modelos personalizados en Open WebUI

| Modelo | Funcion |
|---|---|
| `Stardust-Faro` | Perfil base del Nodo Faro para coordinacion, telemetria y operaciones del proyecto |
| `Stardust-Faro-AutoLearn` | Perfil de aprendizaje y analisis iterativo sujeto a auditoria B.6 y supervision humana |

### Enrutamiento remoto: MixRoute

La integracion remota usa el endpoint OpenAI-compatible:

```text
Base URL: https://api.mixroute.ai/v1
Model ID: auto
API key: variable de entorno; nunca versionar credenciales
```

| Perfil | Uso previsto | Simple | Complex | Ultra |
|---|---|---|---|---|
| `Economy` | MQTT, JSON, telemetria, logs, automatizaciones y pruebas | `deepseek-v4-flash-0731` | `deepseek-v4-flash-0731` | `deepseek-v4-flash-0731` |
| `Auto` | Conversacion tecnica, investigacion y desarrollo general | `deepseek-v4-flash-0731` | `deepseek-v4-flash-0731` | `claude-fable-5` |
| `Critical` | Auditoria B.6, Gaia_Score, arquitectura y cambios de alto impacto | `deepseek-v4-flash-0731` | `glm-5.2` | `kimi-k3` |

### Controles de operacion

- Usar una API key por perfil y definir una cuota maxima por key.
- No almacenar API keys, tokens, IPs privadas ni valores de `.env` en Git.
- Rotar credenciales y configurar expiracion antes de usar servicios remotos persistentes.
- Separar conversaciones de rutina de auditorias criticas para controlar contexto, trazabilidad y costo.
- Todo dictamen Critical requiere evidencia verificable, auditoria cruzada B.6 y revision humana Tlacuilo/Exar Ahau.

---

## Licencia y Adhesion

- **Contenido**: CC0 1.0 Universal (Dominio Publico).
- **Como unirse**:
  1. Abrir un Issue en `bioconexion3i/convocatoriapuentecosmico2027-2079`.
  2. Completar la plantilla de adhesion (tipo: humano, org, IA).
  3. Recibir ID Unico y hash de compromiso.
  4. Integrar nodo o contribuir al framework (codigo, datos, gobernanza).

---

## Proximos Pasos (2025-2026)

1. **Consolidar Nodo Faro Merida**: Estabilizar telemetria MQTT y dashboard Cosmograma.
2. **Auditoria B.6**: Validar coherencia logica de todos los documentos fundacionales.
3. **Despliegue de 100 nodos piloto**: En la peninsula de Yucatan (ESP32+LoRa).
4. **Integracion de IA multiple**: Nemotron-3, LFM2.5, DeepSeek V4 para validacion cruzada.
5. **Primer informe Gaia_Score**: Evaluacion de impacto de actividades humanas en la region.

---

## Contacto y Documentacion

- **Repositorio**: `bioconexion3i/convocatoriapuentecosmico2027-2079`
- **Documentacion tecnica**: `/docs`, `/nodo_merida`, `/stardust-audit`
- **Bitacora de errores**: `ERRORES_IA.md`
- **Adhesiones**: `adhesiones.json` (via Issues)

---

*Este documento es una sintesis viva. Se actualiza con cada hito completado y cada adhesion validada.*